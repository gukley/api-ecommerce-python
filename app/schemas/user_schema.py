from pydantic import BaseModel, EmailStr
from app.models.user_model import UserRole
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserCreateModerator(UserCreate):
    role: Optional[UserRole] = UserRole.MODERATOR


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserImageUpdate(BaseModel):
    image_path: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    image_path: Optional[str]

    class Config:
        model_config = {"from_attributes": True}
