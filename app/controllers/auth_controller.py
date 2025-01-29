from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.core.middlewares.auth_middleware import get_current_user
from app.schemas.login_schema import LoginRequest, LoginResponse

router = APIRouter()


@router.post(
    "/login", summary="Authenticate user and return token", response_model=LoginResponse
)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.authenticate_user(db, login_data.email, login_data.password)


@router.post("/register", summary="Register a new user", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_data)


@router.post("/renew-token", summary="Renew authentication token")
def renew_token(current_user: dict = Depends(get_current_user)):
    new_token = AuthService.renew_token(current_user)
    return {"new_token": new_token}
