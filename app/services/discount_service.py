from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.discount_repository import DiscountRepository
from app.models.discount_model import Discount
from app.schemas.discount_schema import DiscountCreate, DiscountUpdate


class DiscountService:
    @staticmethod
    def get_all_discounts(db: Session) -> list[Discount]:
        return DiscountRepository.get_all_discounts(db)

    @staticmethod
    def get_discount_by_id(db: Session, discount_id: int) -> list[Discount]:
        return DiscountRepository.get_discount_by_id(db, discount_id)

    @staticmethod
    def create_discount(db: Session, discount_data: DiscountCreate) -> Discount:
        discount = Discount(**discount_data.model_dump())
        return DiscountRepository.create_discount(db, discount)

    @staticmethod
    def update_discount(
        db: Session, discount_id: int, discount_data: DiscountUpdate
    ) -> Discount:
        updates = discount_data.model_dump(exclude_unset=True)
        discount = DiscountRepository.update_discount(db, discount_id, updates)
        if not discount:
            raise HTTPException(status_code=404, detail="Discount not found")
        return discount

    @staticmethod
    def delete_discount(db: Session, discount_id: int):
        DiscountRepository.delete_discount(db, discount_id)
