from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timezone
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.core.middlewares.auth_middleware import get_current_user
from app.schemas.login_schema import LoginRequest, LoginResponse
from app.models.user_model import User
from app.services.auth_service import create_access_token, verify_password
from fastapi.security import OAuth2PasswordBearer
from app.services.token_service import create_refresh_token, verify_refresh_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post(
    "/login",
    summary="Autenticar usuário e retornar tokens",
    description="Realiza autenticação do usuário utilizando email e senha, retornando tokens JWT válidos.",
    response_model=LoginResponse,
)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email.ilike(login_data.email)).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Gera o access token e o refresh token
    access_token = create_access_token({"sub": str(user.id), "role": user.role.value if hasattr(user.role, "value") else user.role})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Retorna os tokens e informações do usuário
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # Adicionado para corrigir o erro
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
            "image_path": user.image_path,
            "admin_id": user.admin_id if user.admin_id is not None else None,
        },
    }

@router.post(
    "/register",
    summary="Registrar um novo usuário",
    description="Realiza o registro de um novo usuário no sistema.",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_data)

@router.post(
    "/renew-token",
    summary="Renovar o access token usando o refresh token",
    description="Gera um novo access token usando um refresh token válido.",
)
def renew_token(refresh_token: str):
    user_id = verify_refresh_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado")

    # Gera um novo access token
    new_access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = create_refresh_token({"sub": str(user_id)})  # Opcional
    return {"new_token": new_access_token, "new_refresh_token": new_refresh_token}

@router.get(
    "/verify-token",
    summary="Verificar validade do token JWT",
    description="Verifica se o token JWT fornecido está ativo e válido e retorna o horário de expiração do token.",
    status_code=status.HTTP_200_OK,
)
def verify_token(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "exp"):
        raise HTTPException(status_code=400, detail="Token expiration not found")

    token_expiration = datetime.fromtimestamp(current_user.exp, timezone.utc)
    return {
        "active": True,
        "user_id": current_user.id,
        "expires_at": token_expiration.isoformat(),
    }
