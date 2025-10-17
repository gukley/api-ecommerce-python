from datetime import datetime, timedelta
import jwt
import os

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))  # 15 minutos
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))  # 7 dias
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 30))  # 30 minutos


def create_access_token(data: dict, expires_delta: int = None) -> str:
    """
    Gera um token JWT de acesso com expiração curta.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    """
    Gera um refresh token JWT com expiração longa.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(user_id: int, expires_minutes: int = RESET_TOKEN_EXPIRE_MINUTES) -> str:
    """
    Gera um token JWT para redefinição de senha.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(token: str) -> int:
    """
    Verifica e decodifica um refresh token JWT.
    Retorna o user_id se o token for válido, ou None se for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None

def verify_reset_token(token: str) -> int:
    """
    Verifica e decodifica um token JWT de redefinição de senha.
    Retorna o user_id se o token for válido, ou None se for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None