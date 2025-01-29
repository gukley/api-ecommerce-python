from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    street: str
    number: int
    zip: str
    city: str
    state: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    number: Optional[int] = None
    zip: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        model_config = {"from_attributes": True}
