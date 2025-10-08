import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, CRYPT_ALGORITHM

def create_reset_token(user_id: int, expires_minutes: int = 30):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=CRYPT_ALGORITHM)

def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[CRYPT_ALGORITHM])
        return payload.get("user_id")
    except Exception:
        return None
