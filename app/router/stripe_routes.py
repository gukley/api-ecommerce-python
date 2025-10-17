import os
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import stripe
from dotenv import load_dotenv
from app.utils.email_utils import send_purchase_email
from app.models.order_model import Order, OrderStatus
from app.repositories.order_repository import OrderRepository
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.database import get_db

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/payments", tags=["Payments"])

# Models
class item(BaseModel):
    name: str
    amount: float
    quantity: Optional[int] = 1

class PayerInfo(BaseModel):
    name: str
    tax_id: str  # CPF

class CheckoutPayload(BaseModel):
    items: List[item]
    success_url: Optional[HttpUrl] = None
    cancel_url: Optional[HttpUrl] = None
    email: Optional[str] = None
    metadata: Optional[dict] = None
    payer: Optional[PayerInfo] = None  # Adicionado para boleto

@router.post("/create-checkout-session")
async def create_checkout_session(payload: CheckoutPayload):
    try:
        line_items = []
        for it in payload.items:
            line_items.append({
                "price_data": {
                    "currency": "brl",
                    "product_data": {"name": it.name},
                    "unit_amount": int(round(it.amount * 100))  # em centavos
                },
                "quantity": it.quantity or 1,
            })

        payment_methods = ["card"]
        if payload.payer:  # Se dados do pagador foram enviados, habilita boleto
            payment_methods.append("boleto")

        session = stripe.checkout.Session.create(
            payment_method_types=payment_methods,
            line_items=line_items,
            mode="payment",
            success_url=str(payload.success_url),
            cancel_url=str(payload.cancel_url),
            customer_email=payload.email,
            metadata=payload.metadata or {},
            # Para boleto, o Stripe coleta os dados do pagador na interface do checkout
        )

        return {"url": session.url, "id": session.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        order_id = data.get("metadata", {}).get("order_id")
        user_email = data.get("customer_email")
        print(f"✅ Pedido {order_id} pago com sucesso (checkout.session.completed)")

        db: Session = next(get_db())
        if order_id and user_email:
            order = OrderRepository.get_order_by_id(db, int(order_id))
            if order:
                # Marcar pedido como pago usando Enum
                order.status = OrderStatus.PAID  # Use o valor correto do Enum
                db.commit()
                send_purchase_email(user_email, order)
                
    elif event_type == "payment_intent.succeeded":
        print(f"💳 PaymentIntent {data['id']} confirmado")

    elif event_type == "charge.refunded":
        print(f"🔄 Pagamento {data['payment_intent']} foi reembolsado")

    else:
        print(f"ℹ️ Evento recebido sem tratamento: {event_type}")

    return {"status": "success"}

@router.post("/create-payment-intent")
async def create_payment(payload: CheckoutPayload):
    try:
        amount = sum(int(round(it.amount * 100)) * (it.quantity or 1) for it in payload.items)
        payment_methods = ["card"]
        boleto_options = None
        if payload.payer:
            payment_methods.append("boleto")
            boleto_options = {
                "boleto": {
                    "expires_after_days": 3,  # Opcional: validade do boleto
                }
            }
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="brl",
            payment_method_types=payment_methods,
            metadata=payload.metadata or {},
            receipt_email=payload.email,
            payment_method_options=boleto_options if boleto_options else None,
            # Para boleto, o Stripe coleta os dados do pagador na interface do checkout
        )
        return {"clientSecret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/finance")
async def get_finance_dashboard(db: Session = Depends(get_db)):
    """
    Endpoint para retornar dados financeiros para o dashboard do admin.
    Retorna lista de pagamentos/pedidos com informações relevantes.
    """
    orders = db.query(Order).all()
    result = []
    for order in orders:
        user = db.query(User).filter(User.id == order.user_id).first()
        items = []
        for item in order.order_items:
            items.append({
                "name": item.product.name if item.product else "",
                "quantity": item.quantity,
                "unit_price": float(item.unit_price) * 100,  # em centavos para frontend
            })
        result.append({
            "id": order.id,
            "customer_name": user.name if user else "",
            "customer_email": user.email if user else "",
            "amount": float(order.total_amount) * 100,  # em centavos para frontend
            "payment_method": getattr(order, "payment_method", "Desconhecido"),
            "status": str(order.status).lower(),
            "created_at": order.order_date.isoformat() if order.order_date else "",
            "fee": 0,  # Ajuste se tiver taxa Stripe salva
            "net": float(order.total_amount) * 100,  # Ajuste se descontar taxa
            "items": items,
            "stripe_data": {},  # Preencha se quiser mostrar dados do Stripe
        })
    return result