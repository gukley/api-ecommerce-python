from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.review_schema import ReviewCreate, ReviewUpdate, ReviewResponse
from app.models.user_model import User
from app.services.review_service import ReviewService
from app.core.middlewares.auth_middleware import get_current_user

router = APIRouter()

@router.get("/", response_model=list[ReviewResponse])
def get_reviews(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReviewService.get_reviews(db, current_user)

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def add_review(data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReviewService.add_review(db, current_user, data)

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, data: ReviewUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ReviewService.update_review(db, current_user, review_id, data)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ReviewService.delete_review(db, current_user, review_id)
    return