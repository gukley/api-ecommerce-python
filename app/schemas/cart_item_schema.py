from pydantic import BaseModel, Field
from typing_extensions import Annotated
from decimal import Decimal
from typing import Optional


class CartItemBase(BaseModel):
    cart_id: int
    product_id: int
    quantity: int
    unit_price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]


class CartItemCreate(CartItemBase):
    pass


class CartItemRemove(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    product_id: int
    quantity: int


class CartItemResponse(CartItemBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
