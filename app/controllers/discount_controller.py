from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.discount_schema import DiscountCreate, DiscountResponse, DiscountUpdate
from app.services.discount_service import DiscountService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import UserRole
from app.dependencies.auth import is_admin

router = APIRouter()


@router.get("/", response_model=list[DiscountResponse])
def get_discounts(db: Session = Depends(get_db)):
    return DiscountService.get_all_discounts(db)


@router.get("/{discount_id}", response_model=DiscountResponse)
def get_discount(discount_id: int, db: Session = Depends(get_db)):
    discount = DiscountService.get_discount_by_id(db, discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
    return discount


@router.post("/", response_model=DiscountResponse)
def create_discount(
    discount_data: DiscountCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return DiscountService.create_discount(db, discount_data)


@router.put("/{discount_id}", response_model=DiscountResponse)
def update_discount(
    discount_id: int,
    discount_data: DiscountUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return DiscountService.update_discount(db, discount_id, discount_data)


@router.delete("/{discount_id}", status_code=204)
def delete_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    DiscountService.delete_discount(db, discount_id)
    return
