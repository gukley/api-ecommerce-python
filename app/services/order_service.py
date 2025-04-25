from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.order_repository import OrderRepository
from app.models.order_model import Order, OrderStatus
from app.models.order_item_model import OrderItem
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse
from app.models.user_model import User
from app.services.cart_service import CartService
from app.models.cart_item_model import CartItem
from app.services.coupon_service import CouponService
from app.services.address_service import AddressService
from decimal import Decimal
from app.services.product_service import ProductService
from sqlalchemy.exc import IntegrityError
from app.schemas.product_schema import ProductBase

class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user: User) -> Order:
        cart = CartService.get_cart_items(db, user)

        if not cart.items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        order = OrderService.create_order_entry(db, order_data, user, cart.total_amount)

        OrderService.create_order_items(db, order, cart.items)

        CartService.clear_cart(db, user)

        return order

    @staticmethod
    def create_order_entry(
        db: Session, order_data: OrderCreate, user: User, total_amount: float
    ) -> Order:
        address = AddressService.get_address_by_id(db, user, order_data.address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")

        if order_data.coupon_id:
            coupon = CouponService.get_coupon_by_id(db, order_data.coupon_id)
            total_amount = Decimal(total_amount)
            total_amount = total_amount - (total_amount * coupon.discount_percentage / Decimal(100))

        order = Order(
            **order_data.model_dump(),
            user_id=user.id,
            total_amount=total_amount,
        )
        return OrderRepository.create_order(db, order)

    @staticmethod
    def create_order_items(db: Session, order: Order, cart_items: list[CartItem]):
        order_items = []

        for item in cart_items:
            ProductService.decrease_stock(db, item.product_id, item.quantity)
            order_items.append(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
            )
            
        OrderRepository.create_order_items(db, order_items)

    @staticmethod
    def get_orders_by_user(db: Session, user: User) -> list[Order]:
        return OrderRepository.get_orders_by_user(db, user.id)

    @staticmethod
    def get_order_by_id(db: Session, order_id: int, user: User) -> OrderResponse:
        order = OrderRepository.get_order_by_id(db, order_id, user.id)
        
        items = []
        for item in order.order_items:
            items.append(ProductBase.model_validate(item.product.__dict__))
        print(order.coupon.__dict__)
        return OrderResponse(id=order.id, order_date=order.order_date, address_id=order.address_id, status=order.status, products=items)

    @staticmethod
    def update_order_status(
        db: Session, order_id: int, status: str
    ) -> Order:
        return OrderRepository.update_order_status(db, order_id, status)

    @staticmethod
    def cancel_order(db: Session, order_id: int, user: User):
        return OrderRepository.cancel_order(db, order_id, user.id)
