from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import SECRET_KEY, CRYPT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=CRYPT_ALGORITHM)

def verify_access_token(token: str) -> dict:
    try:
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]

        return jwt.decode(token, SECRET_KEY, algorithms=[CRYPT_ALGORITHM])
    except JWTError:
        return None
