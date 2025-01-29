from pydantic import BaseModel, Field
from typing_extensions import Annotated
from decimal import Decimal
from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    stock: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[Annotated[Decimal, Field(max_digits=10, decimal_places=2)]] = None
    category_id: Optional[int] = None


class ProductUpdateStock(BaseModel):
    stock: Optional[int] = None


class ProductResponse(ProductBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
