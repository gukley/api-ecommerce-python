from pydantic import BaseModel
from typing import Optional
from pydantic.config import ConfigDict


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryImageUpdate(BaseModel):
    image_path: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
