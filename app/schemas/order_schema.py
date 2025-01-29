from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.order_model import OrderStatus
from typing_extensions import Annotated
from decimal import Decimal


class OrderBase(BaseModel):
    user_id: int
    address_id: int
    coupon_id: Optional[int] = None
    status: OrderStatus
    total_amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderResponse(OrderBase):
    id: int
    order_date: datetime

    class Config:
        model_config = {"from_attributes": True}
