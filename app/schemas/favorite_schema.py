from pydantic import BaseModel
from app.schemas.product_schema import ProductResponse

class FavoriteBase(BaseModel):
    product_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    id: int
    product: ProductResponse

    class Config:
        orm_mode = True