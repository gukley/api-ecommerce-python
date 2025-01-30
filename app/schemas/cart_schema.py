from pydantic import BaseModel
from datetime import datetime
from app.schemas.cart_item_schema import CartItemResponse


class CartBase(BaseModel):
    user_id: int


class CartItemsResponse(BaseModel):
    total: float
    items: list[CartItemResponse]


class CartResponse(CartBase):
    id: int

    created_at: datetime

    class Config:
        model_config = {"from_attributes": True}
