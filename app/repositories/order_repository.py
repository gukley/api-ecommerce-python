from sqlalchemy.orm import Session
from app.models.order_model import Order, OrderStatus
from sqlalchemy.orm import joinedload
from app.models.order_item_model import OrderItem

class OrderRepository:
    @staticmethod
    def create_order(db: Session, order: Order) -> Order:
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def create_order_items(db: Session, order_items: list[OrderItem]):
        db.add_all(order_items)
        db.commit()

    @staticmethod
    def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
        return db.query(Order).options(joinedload(Order.order_items)).filter(Order.user_id == user_id).all()

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user_id: int) -> Order:
        return (
            db.query(Order)
            .options(joinedload(Order.order_items))
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )

    @staticmethod
    def update_order_status(
        db: Session, order_id: int, new_status: OrderStatus
    ) -> Order:
        """
        new_status should be an OrderStatus enum (service should convert/validate before calling).
        """
        order = (
            db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )
        if not order:
            return None

        # Only update if the new status is different
        if order.status != new_status:
            order.status = new_status
            try:
                db.add(order)
                db.commit()
                db.refresh(order)
            except Exception:
                db.rollback()
                raise
        return order

    @staticmethod
    def cancel_order(db: Session, order_id: int, user_id: int):
        order = (
            db.query(Order)
            .options(joinedload(Order.order_items).joinedload(OrderItem.product))
            .filter(Order.id == order_id, Order.user_id == user_id)
            .first()
        )
        if order and (
            order.status == OrderStatus.PENDING
            or order.status == OrderStatus.PROCESSING
        ):
            order.status = OrderStatus.CANCELLED  # Use o Enum correto (CANCELLED)
            for item in order.order_items:
                product = item.product
                product.stock += item.quantity
            try:
                db.commit()
                db.refresh(order)
            except Exception:
                db.rollback()
                raise
        return order

    @staticmethod
    def get_all_orders(db: Session) -> list[Order]:
        return db.query(Order).options(joinedload(Order.order_items)).all()
    
    @staticmethod
    def get_all_orders_by_admin(db: Session, admin_id: int) -> list[Order]:
        return db.query(Order).options(joinedload(Order.order_items)).filter(Order.admin_id == admin_id).all()

    @staticmethod
    def get_order_items_by_order_id(db, order_id: int):
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()