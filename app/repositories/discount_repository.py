from sqlalchemy.orm import Session
from app.models.discount_model import Discount


class DiscountRepository:
    @staticmethod
    def get_all_discounts(db: Session) -> list[Discount]:
        return db.query(Discount).all()

    @staticmethod
    def get_discount_by_id(db: Session, discount_id: int) -> Discount:
        return db.query(Discount).filter(Discount.id == discount_id).first()

    @staticmethod
    def create_discount(db: Session, discount: Discount) -> Discount:
        db.add(discount)
        db.commit()
        db.refresh(discount)
        return discount

    @staticmethod
    def update_discount(db: Session, discount_id: int, updates: dict) -> Discount:
        discount = db.query(Discount).filter(Discount.id == discount_id).first()
        if discount:
            for key, value in updates.items():
                setattr(discount, key, value)
            db.commit()
            db.refresh(discount)
        return discount

    @staticmethod
    def delete_discount(db: Session, discount_id: int):
        discount = db.query(Discount).filter(Discount.id == discount_id).first()
        if discount:
            db.delete(discount)
            db.commit()
