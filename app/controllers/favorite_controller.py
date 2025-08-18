from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.favorite_schema import FavoriteCreate, FavoriteResponse
from app.models.user_model import User
from app.services.favorite_service import FavoriteService
from app.core.middlewares.auth_middleware import get_current_user

router = APIRouter()

@router.get("/", response_model=list[FavoriteResponse])
def get_favorites(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return FavoriteService.get_favorites(db, current_user)

@router.post("/", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(data: FavoriteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return FavoriteService.add_favorite(db, current_user, data)

@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(favorite_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    FavoriteService.remove_favorite(db, current_user, favorite_id)
    return