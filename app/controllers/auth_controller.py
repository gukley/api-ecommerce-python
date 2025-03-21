from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.core.middlewares.auth_middleware import get_current_user
from app.schemas.login_schema import LoginRequest, LoginResponse
from app.models.user_model import User
from datetime import datetime, timezone

router = APIRouter()


@router.post(
    "/login",
    summary="Autenticar usuário e retornar token",
    description="Realiza autenticação do usuário utilizando email e senha, retornando um token JWT válido.",
    response_model=LoginResponse,
)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.authenticate_user(db, login_data.email, login_data.password)


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
    summary="Renovar token de autenticação",
    description="Gera e retorna um novo token JWT para o usuário autenticado.",
)
def renew_token(current_user: User = Depends(get_current_user)):
    new_token = AuthService.renew_token(current_user)
    return {"new_token": new_token}


@router.get(
    "/verify-token",
    summary="Verificar validade do token JWT",
    description="Verifica se o token JWT fornecido está ativo e válido e retorna o horário de expiração do token.",
    status_code=status.HTTP_200_OK,
)
def verify_token(current_user: User = Depends(get_current_user)):
    token_expiration = datetime.fromtimestamp(current_user.exp, timezone.utc)
    return {
        "active": True,
        "user_id": current_user.id,
        "expires_at": token_expiration.isoformat(),
    }
