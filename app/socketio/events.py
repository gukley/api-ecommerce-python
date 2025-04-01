from . import sio
from urllib.parse import parse_qs

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


async def notify_new_order(order_id: int):
    for sid in connected_users:
        await sio.emit("new_order", {"order_id": order_id}, to=sid)
