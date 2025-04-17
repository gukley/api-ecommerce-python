from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.product_schema import ProductResponse

class TagBase(BaseModel):
    code: str
    color_hex: str
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    code: Optional[str] = None
    color_hex: Optional[str] = None
    description: Optional[str] = None

class TagResponse(TagBase):
    id: int
    products: list[ProductResponse]

    class Config:
        model_config = {"from_attributes": True}
