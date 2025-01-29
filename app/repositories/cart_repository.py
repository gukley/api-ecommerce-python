from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.models.cart_item_model import CartItem


class CartRepository:
    @staticmethod
    def get_cart_by_user(db: Session, user_id: int) -> Cart:
        return db.query(Cart).filter(Cart.user_id == user_id).first()

    @staticmethod
    def get_cart_items(db: Session, cart_id: int) -> list[CartItem]:
        return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    @staticmethod
    def add_item_to_cart(db: Session, cart_item: CartItem) -> CartItem:
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

    @staticmethod
    def remove_item_from_cart(db: Session, cart_id: int, product_id: int) -> CartItem:
        cart_item = (
            db.query(CartItem)
            .filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
            .first()
        )
        if cart_item:
            db.delete(cart_item)
            db.commit()

    @staticmethod
    def create_cart(db: Session, cart: Cart) -> Cart:
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart

    @staticmethod
    def clear_cart(db: Session, cart_id: int):
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        db.commit()
