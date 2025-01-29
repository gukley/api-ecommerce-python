from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService
from app.models.user_model import User
from app.dependencies.auth import is_admin

router = APIRouter()


@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return CategoryService.get_all_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryService.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin),
):
    return CategoryService.create_category(db, category_data)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(is_admin),
):
    return CategoryService.update_category(db, category_id, category_data)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int, db: Session = Depends(get_db), _: User = Depends(is_admin)
):
    CategoryService.delete_category(db, category_id)
    return
