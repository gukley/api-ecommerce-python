from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.cart_repository import CartRepository
from app.models.cart_model import Cart
from app.models.user_model import User
from app.schemas.cart_item_schema import (
    CartItemCreate,
    CartItemRemove,
    CartItemUpdate,
    CartItemResponse,
)
from app.schemas.cart_schema import CartItemsResponse
from app.models.cart_item_model import CartItem
from app.services.product_service import ProductService


class CartService:
    @staticmethod
    def get_cart_by_user(db: Session, user: User) -> Cart:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart

    @staticmethod
    def get_cart_items(db: Session, user: User) -> CartItemsResponse:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        total = 0
        items = []

        for item in cart.cart_items:
            total += item.quantity * item.unit_price
            item.image_path = ProductService.get_product_image_path(db, item.product_id)
            items.append(CartItemResponse.model_validate(item.__dict__))

        return CartItemsResponse(cart_id=cart.id, items=items, total_amount=total)

    @staticmethod
    def create_cart(db: Session, user: User) -> Cart:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            cart = Cart(user_id=user.id)
            return CartRepository.create_cart(db, cart)
        return cart

    @staticmethod
    def add_item_to_cart(db: Session, cart_item: CartItemCreate, user: User) -> Cart:
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        product = ProductService.get_product_by_id(db, cart_item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.stock < cart_item.quantity or product.stock == 0:
            raise HTTPException(status_code=400, detail="Not enough stock")

        cart_item = CartItem(
            **cart_item.model_dump(exclude={"unit_price"}),
            unit_price=product.price,
            cart_id=cart.id
        )

        CartRepository.add_item_to_cart(db, cart_item)

        return cart

    @staticmethod
    def remove_item_from_cart(db: Session, cart_item: CartItemRemove, user: User):
        cart = CartRepository.get_cart_by_user(db, user.id)
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        CartRepository.remove_item_from_cart(
            db, cart.id, cart_item.product_id
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
            raise HTTPException(status_code=404, detail="Cart not found")

        CartRepository.update_item_quantity(
            db, cart, cart_item.product_id, cart_item.quantity
        )
