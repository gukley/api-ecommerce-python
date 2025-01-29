from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.cart_repository import CartRepository
from app.models.cart_model import Cart
from app.schemas.cart_schema import CartCreate
from app.models.user_model import User
from app.schemas.cart_item_schema import CartItemCreate, CartItemRemove, CartItemUpdate
from app.models.cart_item_model import CartItem


class CartService:
    @staticmethod
    def get_cart_by_user(db: Session, user: User) -> Cart:
        return CartRepository.get_cart_by_user(db, user.id)

    @staticmethod
    def get_cart_items(db: Session, user: User) -> list[CartItem]:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            return HTTPException(status_code=404, detail="Cart not found")
        return CartRepository.get_cart_items(db, cart.id)

    @staticmethod
    def create_cart(db: Session, cart_data: CartCreate, user: User) -> Cart:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            cart_data.user_id = user.id
            cart = Cart(**cart_data.model_dump())
            return CartRepository.create_cart(db, cart)
        return cart

    @staticmethod
    def add_item_to_cart(db: Session, cart_item: CartItemCreate, user: User) -> Cart:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            return HTTPException(status_code=404, detail="Cart not found")
        cart_item = CartItem(**cart_item.model_dump())
        CartRepository.add_item_to_cart(db, cart_item, cart.id)

    @staticmethod
    def remove_item_from_cart(db: Session, cart_item: CartItemRemove, user: User):
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            return HTTPException(status_code=404, detail="Cart not found")
        CartRepository.remove_item_from_cart(
            db, cart_item.cart_id, cart_item.product_id
        )

    @staticmethod
    def clear_cart(db: Session, user: User):
        cart = CartRepository.get_cart_by_user(db, user.id)
        if cart:
            CartRepository.clear_cart(db, cart.id)

    @staticmethod
    def update_item_quantity(db: Session, cart_item: CartItemUpdate, user: User):
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            return HTTPException(status_code=404, detail="Cart not found")

        CartRepository.update_item_quantity(
            db, cart, cart_item.product_id, cart_item.quantity
        )
