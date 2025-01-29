from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.models.order_model import Order
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.models.user_model import User


class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> Order:
        order = Order(**order_data.model_dump())
        return OrderRepository.create_order(db, order)

    @staticmethod
    def get_orders_by_user(db: Session, user: User) -> list[Order]:
        return OrderRepository.get_orders_by_user(db, user.id)

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user: User) -> Order:
        order = OrderRepository.get_order_by_id(db, order_id, user.id)
        if order:
            return order
        return None

    @staticmethod
    def update_order_status(
        db: Session, order_id: int, status: str, user: User
    ) -> Order:
        return OrderRepository.update_order_status(db, order_id, status, user.id)

    @staticmethod
    def cancel_order(db: Session, order_id: int, user: User):
        return OrderRepository.cancel_order(db, order_id, user.id)
