from pydantic import BaseModel
from datetime import datetime


class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass


class CartResponse(CartBase):
    id: int
    created_at: datetime

    class Config:
        model_config = {"from_attributes": True}
