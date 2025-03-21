from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.core.middlewares.auth_middleware import get_current_user
from app.schemas.login_schema import LoginRequest, LoginResponse
from app.models.user_model import User

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
