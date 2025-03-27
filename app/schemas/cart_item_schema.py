from pydantic import BaseModel


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

    class Config:
        model_config = {"from_attributes": True}
