from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from app.core.middlewares.auth_middleware import get_current_user
from app.models.user_model import User

router = APIRouter()


@router.get("/", response_model=list[OrderResponse])
def get_orders(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return OrderService.get_orders_by_user(db, current_user)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = OrderService.get_order_by_id(db, order_id, current_user)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.create_order(db, order_data, current_user)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return OrderService.update_order_status(
        db, order_id, order_data.status, current_user
    )


@router.delete("/{order_id}", status_code=204)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    OrderService.cancel_order(db, order_id, current_user)
    return
