from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order_model import OrderStatus
from app.schemas.product_schema import ProductBase
from pydantic import ConfigDict
from decimal import Decimal
from typing_extensions import Annotated

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class OrderBase(BaseModel):
    address_id: int
    coupon_id: Optional[int] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    payment_method: str
    total_amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    shipping_cost: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None

class OrderResponse(OrderBase):
    id: int
    order_date: datetime
    status: OrderStatus
    products: Optional[list[ProductBase]] = None
    user_id: int

    model_config = ConfigDict(from_attributes=True)