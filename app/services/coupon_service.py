from sqlalchemy.orm import Session
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
        coupon = Coupon(**coupon_data.dict())
        return CouponRepository.create_coupon(db, coupon)

    @staticmethod
    def update_coupon(db: Session, coupon_id: int, coupon_data: CouponUpdate) -> Coupon:
        updates = coupon_data.dict(exclude_unset=True)
        return CouponRepository.update_coupon(db, coupon_id, updates)

    @staticmethod
    def delete_coupon(db: Session, coupon_id: int):
        CouponRepository.delete_coupon(db, coupon_id)
