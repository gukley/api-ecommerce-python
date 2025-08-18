from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.product_schema import ProductResponse

class ReviewBase(BaseModel):
    product_id: int
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    product: ProductResponse

    class Config:
        orm_mode = True