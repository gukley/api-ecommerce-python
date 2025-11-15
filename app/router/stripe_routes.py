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

class ConfirmPaymentPayload(BaseModel):
    order_id: int
    payment_intent_id: Optional[str] = None
    method: Optional[str] = "card"

def _safe_set(order_obj, attr_name, value):
    """
    Set attribute only if it exists on the SQLAlchemy model to avoid AttributeError
    when models don't have the optional columns.
    """
    if hasattr(order_obj, attr_name):
        setattr(order_obj, attr_name, value)

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

        # Cria a Session do Checkout. Importante: passar metadata também para o PaymentIntent
        # usando payment_intent_data para que o PaymentIntent carregue a mesma metadata.
        session = stripe.checkout.Session.create(
            payment_method_types=payment_methods,
            line_items=line_items,
            mode="payment",
            success_url=str(payload.success_url) if payload.success_url else None,
            cancel_url=str(payload.cancel_url) if payload.cancel_url else None,
            customer_email=payload.email,
            metadata=payload.metadata or {},
            payment_intent_data={"metadata": payload.metadata or {}, "receipt_email": payload.email} if (payload.metadata or payload.email) else None,
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

    # Obtém sessão DB
    db: Session = next(get_db())

    # --- 1) Quando a Checkout Session é finalizada pelo cliente (mas boleto pode ainda estar PENDING) ---
    if event_type == "checkout.session.completed":
        session = data
        order_id = session.get("metadata", {}).get("order_id")
        user_email = session.get("customer_email")
        stripe_pi = session.get("payment_intent")  # id do PaymentIntent criado pela Session (pode existir)

        print(f"✅ checkout.session.completed: session={session.get('id')} order_id={order_id} payment_intent={stripe_pi}")

        if order_id:
            order = OrderRepository.get_order_by_id(db, int(order_id))
            if order:
                pm_types = session.get("payment_method_types", [])
                if "boleto" in pm_types:
                    order.status = OrderStatus.PENDING  # boleto precisa confirmação assíncrona
                    _safe_set(order, "payment_method", "boleto")
                else:
                    order.status = OrderStatus.PAID
                    _safe_set(order, "payment_method", "card")
                if stripe_pi:
                    _safe_set(order, "stripe_payment_intent", stripe_pi)
                _safe_set(order, "stripe_session_id", session.get("id"))
                db.commit()
                try:
                    # Envia e-mail de confirmação/instruções (no boleto você pode enviar com instruções)
                    send_purchase_email(user_email, order)
                except Exception as e:
                    print("Erro ao enviar email:", e)

    # --- 2) Eventos de pagamento assíncrono do Checkout (ex.: boleto) ---
    elif event_type == "checkout.session.async_payment_succeeded":
        session = data
        order_id = session.get("metadata", {}).get("order_id")
        stripe_pi = session.get("payment_intent")
        print(f"✅ checkout.session.async_payment_succeeded: session={session.get('id')} order_id={order_id} payment_intent={stripe_pi}")

        if order_id:
            order = OrderRepository.get_order_by_id(db, int(order_id))
            if order and order.status != OrderStatus.PAID:
                order.status = OrderStatus.PAID
                _safe_set(order, "payment_method", getattr(order, "payment_method", "boleto") or "boleto")
                if stripe_pi:
                    _safe_set(order, "stripe_payment_intent", stripe_pi)
                db.commit()
                try:
                    send_purchase_email(order.user.email, order)
                except Exception as e:
                    print("Erro ao enviar email:", e)

    elif event_type == "checkout.session.async_payment_failed":
        session = data
        order_id = session.get("metadata", {}).get("order_id")
        print(f"❌ checkout.session.async_payment_failed: session={session.get('id')} order_id={order_id}")
        if order_id:
            order = OrderRepository.get_order_by_id(db, int(order_id))
            if order:
                # Marque como failed/cancelled conforme seu modelo (aqui uso FAILED quando existir)
                try:
                    order.status = OrderStatus.FAILED
                except Exception:
                    # se não existir o enum/valor, tenta CANCELLED
                    try:
                        order.status = OrderStatus.CANCELLED
                    except Exception:
                        order.status = OrderStatus.PENDING
                db.commit()

    # --- 3) Fallback: PaymentIntent.succeeded (muitas vezes é emitido quando o pagamento é confirmado) ---
    elif event_type == "payment_intent.succeeded":
        pi = data
        payment_intent_id = pi.get("id")
        metadata = pi.get("metadata", {}) or {}
        order_id = metadata.get("order_id")
        print(f"💳 payment_intent.succeeded: pi={payment_intent_id} metadata.order_id={order_id}")

        # Se metadata não estiver no PI, tente recuperar a Checkout Session relacionada
        if not order_id and payment_intent_id:
            try:
                sessions = stripe.checkout.Session.list(payment_intent=payment_intent_id, limit=1)
                if sessions and sessions.data:
                    sess = sessions.data[0]
                    order_id = sess.get("metadata", {}).get("order_id")
                    print(f"  -> Encontrado order_id via session {sess.get('id')}: {order_id}")
            except Exception as e:
                print("Erro ao buscar session por payment_intent:", e)

        # Inferir método de pagamento (card/boleto) a partir do PaymentIntent ou charge
        inferred_method = None
        try:
            pm_types = pi.get("payment_method_types", []) or []
            if "card" in pm_types:
                inferred_method = "card"
            elif "boleto" in pm_types:
                inferred_method = "boleto"
            # fallback: verificar charges -> payment_method_details
            charges = pi.get("charges", {}).get("data", []) if isinstance(pi.get("charges", {}), dict) else []
            if charges and not inferred_method:
                ch = charges[0]
                pmd = ch.get("payment_method_details", {}) or {}
                ptype = pmd.get("type")
                if ptype:
                    inferred_method = ptype.lower()
        except Exception as e:
            print("Erro ao inferir método do PaymentIntent:", e)

        if order_id:
            order = OrderRepository.get_order_by_id(db, int(order_id))
            if order and order.status != OrderStatus.PAID:
                order.status = OrderStatus.PAID
                # Se já existir payment_method no pedido, não sobrescrever; caso contrário, usa o inferido ou 'card' por padrão
                current_pm = getattr(order, "payment_method", None)
                if current_pm:
                    _safe_set(order, "payment_method", (current_pm or "").lower())
                else:
                    _safe_set(order, "payment_method", inferred_method or "card")
                _safe_set(order, "stripe_payment_intent", payment_intent_id)
                db.commit()
                try:
                    send_purchase_email(order.user.email, order)
                except Exception as e:
                    print("Erro ao enviar email:", e)

    # --- 4) Outras notificações úteis ---
    elif event_type == "charge.refunded":
        print(f"🔄 charge.refunded para payment_intent={data.get('payment_intent')}")
        # Você pode buscar order via metadata do charge, se preenchido:
        try:
            order_id = data.get("metadata", {}).get("order_id")
            if order_id:
                order = OrderRepository.get_order_by_id(db, int(order_id))
                if order:
                    try:
                        order.status = OrderStatus.REFUNDED
                    except Exception:
                        order.status = OrderStatus.PENDING
                    db.commit()
        except Exception as e:
            print("Erro ao processar refund webhook:", e)

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
        return {"clientSecret": intent.client_secret, "id": intent.id}
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

        # Normaliza status para string simples (ex: "pending", "paid", "completed")
        try:
            status_val = order.status.name.lower()
        except Exception:
            status_val = str(order.status).lower() if order.status is not None else "unknown"

        # Normaliza payment_method (garante lowercase ou 'desconhecido')
        pm = getattr(order, "payment_method", None)
        if pm:
            payment_method_val = str(pm).lower()
        else:
            payment_method_val = "desconhecido"

        result.append({
            "id": order.id,
            "customer_name": user.name if user else "",
            "customer_email": user.email if user else "",
            "customer_cpf": user.cpf if user else "-",  # Adicionado CPF
            "customer_phone": user.phone if user else "-",  # Adicionado telefone
            "amount": float(order.total_amount) * 100,  # em centavos para frontend
            "payment_method": payment_method_val,
            "status": status_val,
            "created_at": order.order_date.isoformat() if order.order_date else "",
            "fee": 0,  # Ajuste se tiver taxa Stripe salva
            "net": float(order.total_amount) * 100,  # Ajuste se descontar taxa
            "items": items,
            "stripe_data": {
                "stripe_session_id": getattr(order, "stripe_session_id", None),
                "stripe_payment_intent": getattr(order, "stripe_payment_intent", None)
            },  # Preencha se quiser mostrar dados do Stripe
        })
    return result

@router.post("/confirm-payment")
async def confirm_payment_manual(payload: ConfirmPaymentPayload):
    """
    Endpoint para o frontend confirmar imediatamente um pagamento (hotfix).
    Ex: { order_id: 123, payment_intent_id: "pi_...", method: "card" }
    """
    db: Session = next(get_db())
    order = OrderRepository.get_order_by_id(db, int(payload.order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    try:
        order.status = OrderStatus.PAID
        # grava method e payment intent se colunas existirem
        if hasattr(order, "payment_method"):
            order.payment_method = (payload.method or "card").lower()
        if hasattr(order, "stripe_payment_intent") and payload.payment_intent_id:
            order.stripe_payment_intent = payload.payment_intent_id
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar pedido: {e}")

    try:
        # opcional: enviar email de confirmação
        send_purchase_email(order.user.email, order)
    except Exception:
        pass

    return {"status": "ok", "order_id": order.id}