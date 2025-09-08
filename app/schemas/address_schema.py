from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    street: str
    number: int
    zip: str  # já é string, só garantir no front que são 8 dígitos
    bairro: str  # novo campo
    city: str
    state: str
    country: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    number: Optional[int] = None
    zip: Optional[str] = None
    bairro: Optional[str] = None  # novo campo
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        model_config = {"from_attributes": True}
