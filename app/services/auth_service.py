from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.security import verify_password, hash_password
from app.core.jwt import create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.models.user_model import User


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> str:
        user = UserRepository.get_user_by_email(db, email)

        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token_data = {"sub": user.email, "role": user.role.value}
        token = create_access_token(token_data)
        return {"token": token, "user": user}

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_user = UserRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data.password = hash_password(user_data.password)
        user = User(**user_data.model_dump())
        return UserRepository.create_user(db, user)

    @staticmethod
    def renew_token(current_user: User) -> str:
        token_data = {"sub": current_user.email, "role": current_user.role.value}
        new_token = create_access_token(token_data)
        return new_token
