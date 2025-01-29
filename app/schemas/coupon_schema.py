from pydantic import BaseModel, Field
from datetime import datetime
from typing_extensions import Annotated
from decimal import Decimal
from typing import Optional


class CouponBase(BaseModel):
    code: str
    discount_percentage: Annotated[Decimal, Field(max_digits=5, decimal_places=2)]
    start_date: datetime
    end_date: datetime


class CouponCreate(CouponBase):
    pass


class CouponUpdate(CouponBase):
    code: Optional[str] = None
    discount_percentage: Optional[
        Annotated[Decimal, Field(max_digits=5, decimal_places=2)]
    ] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class CouponResponse(CouponBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
