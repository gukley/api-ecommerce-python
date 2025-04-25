from . import sio
from urllib.parse import parse_qs
from app.schemas.order_schema import OrderResponse, OrderBase
from app.models.order_model import Order

connected_users = {}

@sio.event
async def connect(sid, environ):
    query = parse_qs(environ["asgi.scope"]["query_string"].decode())
    user_id = query.get("user_id", [None])[0]

    if user_id:
        connected_users[sid] = int(user_id)
        print(f"✅ Moderator conectado: {user_id} (sid: {sid})")
    else:
        print("❌ Conexão sem user_id, desconectando.")
        await sio.disconnect(sid)

@sio.event
async def disconnect(sid):
    user_id = connected_users.pop(sid, None)
    if user_id:
        print(f"🔌 Moderator desconectado: {user_id} (sid: {sid})")


async def notify_new_order(order: Order):
    order_data = OrderResponse.model_validate(order).model_dump(mode="json")

    for sid in connected_users:
        await sio.emit("new_order", {"order": order_data}, to=sid)
