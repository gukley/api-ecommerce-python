from pydantic import BaseModel, Field
from typing_extensions import Annotated
from decimal import Decimal
from typing import Optional
from app.schemas.category_schema import CategoryResponse
from app.schemas.discount_schema import DiscountResponse


class ProductBase(BaseModel):
    name: str
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    stock: int
    category_id: int
    image_path: Optional[str] = None
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Annotated[Decimal, Field(max_digits=10, decimal_places=2)]] = None
    category_id: Optional[int] = None


class ProductUpdateStock(BaseModel):
    stock: Optional[int] = None


class ProductResponse(ProductBase):
    id: int
    category: CategoryResponse
    discounts: list[DiscountResponse]

    class Config:
        model_config = {"from_attributes": True}
