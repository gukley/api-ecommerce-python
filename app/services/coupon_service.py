from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.coupon_repository import CouponRepository
from app.models.coupon_model import Coupon
from app.schemas.coupon_schema import CouponCreate, CouponUpdate


class CouponService:
    @staticmethod
    def get_all_coupons(db: Session) -> list[Coupon]:
        return CouponRepository.get_all_coupons(db)

    @staticmethod
    def get_coupon_by_id(db: Session, coupon_id: int) -> Coupon:
        return CouponRepository.get_coupon_by_id(db, coupon_id)

    @staticmethod
    def create_coupon(db: Session, coupon_data: CouponCreate) -> Coupon:
        if coupon_data.discount_percentage > 100 or coupon_data.discount_percentage < 1:
            raise HTTPException(
                status_code=400, detail="Discount percentage must be between 1 and 100"
            )

        coupon = Coupon(**coupon_data.model_dump())

        if CouponRepository.get_coupon_by_code(db, coupon.code):
            raise HTTPException(status_code=400, detail="Coupon code already exists")

        return CouponRepository.create_coupon(db, coupon)

    @staticmethod
    def update_coupon(db: Session, coupon_id: int, coupon_data: CouponUpdate) -> Coupon:
        updates = coupon_data.model_dump(exclude_unset=True)
        coupon = CouponRepository.get_coupon_by_id(db, coupon_id)
        if not coupon:
            raise HTTPException(status_code=404, detail="Coupon not found")

        coupon = CouponRepository.get_coupon_by_code(db, coupon_data.code)
        if coupon:
            raise HTTPException(status_code=400, detail="Coupon code already exists")

        return CouponRepository.update_coupon(db, coupon_id, updates)

    @staticmethod
    def delete_coupon(db: Session, coupon_id: int):
        CouponRepository.delete_coupon(db, coupon_id)
