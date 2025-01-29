from sqlalchemy.orm import Session
from app.models.coupon_model import Coupon


class CouponRepository:
    @staticmethod
    def get_coupon_by_id(db: Session, coupon_id: int) -> Coupon:
        return db.query(Coupon).filter(Coupon.id == coupon_id).first()

    @staticmethod
    def get_all_coupons(db: Session) -> list[Coupon]:
        return db.query(Coupon).all()

    @staticmethod
    def get_coupon_by_code(db: Session, coupon_code: str) -> Coupon:
        return db.query(Coupon).filter(Coupon.code == coupon_code).first()

    @staticmethod
    def create_coupon(db: Session, coupon: Coupon) -> Coupon:
        db.add(coupon)
        db.commit()
        db.refresh(coupon)
        return coupon

    @staticmethod
    def update_coupon(db: Session, coupon_id: int, updates: dict) -> Coupon:
        coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
        if coupon:
            for key, value in updates.items():
                setattr(coupon, key, value)
            db.commit()
            db.refresh(coupon)
        return coupon

    @staticmethod
    def delete_coupon(db: Session, coupon_id: int):
        coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
        if coupon:
            db.delete(coupon)
            db.commit()
