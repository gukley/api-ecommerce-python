from pydantic import BaseModel


class ProductDiscountBase(BaseModel):
    product_id: int
    discount_id: int


class ProductDiscountCreate(ProductDiscountBase):
    pass


class ProductDiscountResponse(ProductDiscountBase):
    id: int

    class Config:
        model_config = {"from_attributes": True}
