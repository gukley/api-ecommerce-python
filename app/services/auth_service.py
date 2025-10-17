from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import verify_password, hash_password
from app.services.token_service import create_access_token, verify_refresh_token
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.models.user_model import User
from datetime import datetime, timedelta
import jwt
import os


SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))  # 7 dias


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> dict:
        user = UserRepository.get_user_by_email(db, email)

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token_data = {"sub": str(user.id), "role": user.role.value}
        access_token = create_access_token(token_data)
        refresh_token = AuthService.create_refresh_token(token_data)
        return {"access_token": access_token, "refresh_token": refresh_token, "user": user}

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_user = UserRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data.password = hash_password(user_data.password)
        user = User(**user_data.model_dump())
        return UserRepository.create_user(db, user)

    @staticmethod
    def renew_token(refresh_token: str) -> dict:
        user_id = verify_refresh_token(refresh_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        token_data = {"sub": str(user_id)}
        new_access_token = create_access_token(token_data)
        new_refresh_token = AuthService.create_refresh_token(token_data)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}

    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        Gera um refresh token JWT com os dados fornecidos.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return refresh_token
