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


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    user_id: int
    product_count: int = 0  # Novo campo
    
    class Config:
        orm_mode = True
