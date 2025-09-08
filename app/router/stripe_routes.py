import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/payments", tags=["Payments"])

# Models
class item(BaseModel):
    name: str
    amount: float
    quantity: Optional[int] = 1

class CheckoutPayload(BaseModel):
    items: List[item]
    success_url: HttpUrl
    cancel_url: HttpUrl
    email: Optional[str] = None
    metadata: Optional[dict] = None

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

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=str(payload.success_url),
            cancel_url=str(payload.cancel_url),
            customer_email=payload.email,
            metadata=payload.metadata or {}
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

    # --- Tratamento de eventos ---
    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        order_id = data.get("metadata", {}).get("order_id")
        print(f"✅ Pedido {order_id} pago com sucesso (checkout.session.completed)")
        # Aqui você pode atualizar no seu DB: status = "paid"

    elif event_type == "payment_intent.succeeded":
        print(f"💳 PaymentIntent {data['id']} confirmado")

    elif event_type == "charge.refunded":
        print(f"🔄 Pagamento {data['payment_intent']} foi reembolsado")

    else:
        print(f"ℹ️ Evento recebido sem tratamento: {event_type}")

    return {"status": "success"}
