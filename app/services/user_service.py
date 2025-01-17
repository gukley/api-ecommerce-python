from sqlalchemy.orm import Session
from app.repositories.user_repository import create_user, get_user, get_users
from app.schemas.user_schema import UserCreate

def create_new_user(db: Session, data: UserCreate):
    return create_user(db, data)

def get_user_by_id(db: Session, user_id: int):
    return get_user(db, user_id)

def list_all_users(db: Session):
    return get_users(db)
