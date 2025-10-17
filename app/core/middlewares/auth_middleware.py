from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt
from app.database import get_db
from app.core.config import SECRET_KEY, ALGORITHM
from app.models.user_model import User  # Corrija o caminho para o arquivo correto
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logger = logging.getLogger(__name__)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")

    try:
        # remove prefixo "Bearer " caso venha nesse formato
        if isinstance(token, str) and token.startswith("Bearer "):
            token = token.split(" ", 1)[1]

        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido ou formato incorreto")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception:
        logger.exception("Erro ao decodificar token")
        raise HTTPException(status_code=401, detail="Falha ao processar token")

    # converte user_id para inteiro de forma segura
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(status_code=401, detail="Token com 'sub' inválido")

    try:
        user = db.query(User).filter(User.id == uid).first()
    except Exception:
        logger.exception("Erro ao buscar usuário no banco")
        raise HTTPException(status_code=500, detail="Erro ao acessar o banco de dados")

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user