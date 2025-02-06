from pydantic import BaseModel, Field
from datetime import datetime
from typing_extensions import Annotated
from decimal import Decimal
from typing import Optional


class DiscountBase(BaseModel):
    description: str
    discount_percentage: Annotated[Decimal, Field(max_digits=5, decimal_places=2)]
    start_date: datetime
    end_date: datetime
    product_id: int


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(BaseModel):
    description: Optional[str] = None
    discount_percentage: Optional[
        Annotated[Decimal, Field(max_digits=5, decimal_places=2)]
    ] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    product_id: Optional[int] = None


class DiscountResponse(DiscountBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
