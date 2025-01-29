from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserResponse, UserUpdate, UserCreateModerator
from app.services.user_service import UserService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_user = UserService.update_user(db, current_user, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_orm(updated_user)


@router.delete("/me", status_code=204)
def delete_me(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    UserService.delete_user(db, current_user)
    return


@router.post("/create-moderator", response_model=UserResponse)
def create_moderator(
    user_data: UserCreateModerator,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return UserService.create_moderator(db, user_data, current_user)
