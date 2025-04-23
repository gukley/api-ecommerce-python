from pydantic import BaseModel
from typing import Optional
from app.schemas.product_schema import ProductResponse

class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class CartItemCreate(CartItemBase):
    pass


class CartItemRemove(BaseModel):
    product_id: int


class CartItemUpdate(BaseModel):
    product_id: int
    quantity: int


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    image_path: Optional[str]
    name: str

    class Config:
        model_config = {"from_attributes": True}
