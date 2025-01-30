from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cart_schema import CartResponse
from app.services.cart_service import CartService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User
from app.schemas.cart_item_schema import (
    CartItemCreate,
    CartItemRemove,
    CartItemUpdate,
)

from app.schemas.cart_schema import CartItemsResponse

router = APIRouter()


@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return CartService.get_cart_by_user(db, current_user)


@router.get("/items", response_model=CartItemsResponse)
def get_cart_items(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return CartService.get_cart_items(db, current_user)


@router.post("/items", status_code=204)
def add_item_to_cart(
    cart_item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CartService.add_item_to_cart(db, cart_item, current_user)


@router.post("/", response_model=CartResponse)
def create_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return CartService.create_cart(db, current_user)


@router.delete("/items", status_code=204)
def remove_item_from_cart(
    cart_item: CartItemRemove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    CartService.remove_item_from_cart(db, cart_item, current_user)
    return


@router.delete("/clear", status_code=204)
def clear_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    CartService.clear_cart(db, current_user)
    return


@router.put("/items", status_code=204)
def update_cart_items(
    cart_item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    CartService.update_item_quantity(db, cart_item, current_user)
    return
