from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.order_model import OrderStatus
from app.schemas.product_schema import ProductBase

class OrderBase(BaseModel):
    address_id: int
    coupon_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderResponse(OrderBase):
    id: int
    order_date: datetime
    status: OrderStatus
    products: Optional[list[ProductBase]] = None

    class Config:
        model_config = {"from_attributes": True}
