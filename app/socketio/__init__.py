import socketio

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socketio_app = socketio.ASGIApp(sio, socketio_path="socket")

__all__ = ["sio", "socketio_app"]
