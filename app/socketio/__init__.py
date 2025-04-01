import socketio

sio = socketio.AsyncServer(cors_allowed_origins="*")
socketio_app = socketio.ASGIApp(sio)

__all__ = ["sio", "socketio_app"]
