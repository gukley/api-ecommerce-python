from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    image_path: Optional[str] = None
    admin_id: Optional[int] = None

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = 'CLIENT'

class UserCreateModerator(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = 'MODERATOR'

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

class UserImageUpdate(BaseModel):
    image_path: Optional[str] = None

class UserInDB(UserResponse):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
    email: str
    role: str

class UserSummary(BaseModel):
    total_orders: int
    total_spent: float
    total_products: int
    total_categories: int
    total_favorites: int
    total_reviews: int
    total_addresses: int
    role: str
    image_path: Optional[str] = None

class ModeratorResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    image_path: Optional[str] = None

class ModeratorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ModeratorUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]