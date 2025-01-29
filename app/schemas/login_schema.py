from pydantic import BaseModel, EmailStr
from app.schemas.user_schema import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse
