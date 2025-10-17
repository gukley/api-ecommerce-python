from pydantic import BaseModel, EmailStr
from typing import Any, Dict, Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    image_path: Optional[str] = None
    admin_id: Optional[int] = None  # Permite que admin_id seja None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str  # Adicionado para incluir o refresh token
    token_type: str
    user: UserResponse
