from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.coupon_schema import CouponCreate, CouponResponse, CouponUpdate
from app.services.coupon_service import CouponService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import UserRole
from app.dependencies.auth import is_admin

router = APIRouter()


@router.get("/", response_model=list[CouponResponse])
def get_coupons(db: Session = Depends(get_db)):
    return CouponService.get_all_coupons(db)


@router.get("/{coupon_id}", response_model=CouponResponse)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = CouponService.get_coupon_by_id(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon


@router.post("/", response_model=CouponResponse)
def create_coupon(
    coupon_data: CouponCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return CouponService.create_coupon(db, coupon_data)


@router.put("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    coupon_id: int,
    coupon_data: CouponUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return CouponService.update_coupon(db, coupon_id, coupon_data)


@router.delete("/{coupon_id}", status_code=204)
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    CouponService.delete_coupon(db, coupon_id)
    return
