from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserUpdate, UserCreateModerator
from app.core.security import hash_password
from fastapi import HTTPException


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return UserRepository.get_user_by_email(db, email)

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return UserRepository.get_user_by_id(db, user_id)

    @staticmethod
    def update_user(db: Session, current_user: User, user_data: UserUpdate) -> User:
        updates = user_data.model_dump(exclude_unset=True)
        if "email" in updates and updates["email"] != current_user.email:
            existing_user = (
                db.query(User).filter(User.email == updates["email"]).first()
            )
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        return UserRepository.update_user(db, current_user.id, updates)

    @staticmethod
    def delete_user(db: Session, current_user: User):
        UserRepository.delete_user(db, current_user.id)

    @staticmethod
    def create_moderator(
        db: Session, user_data: UserCreateModerator, current_user: User
    ) -> User:
        if current_user.role.value != UserRole.ADMIN.value:
            raise HTTPException(
                status_code=403, detail="Not authorized to create a moderator"
            )

        existing_user = UserRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data.password = hash_password(user_data.password)
        user = User(**user_data.model_dump())
        return UserRepository.create_user(db, user)
