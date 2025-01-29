from pydantic import BaseModel, Field
from typing_extensions import Annotated
from decimal import Decimal


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
