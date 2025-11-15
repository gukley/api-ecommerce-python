from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import date
from app.utils.validators import normalize_cpf, validate_cpf, validate_and_format_phone, validate_birthdate, format_cpf_masked

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    image_path: Optional[str] = None
    admin_id: Optional[int] = None

    # Novos campos
    cpf: Optional[str] = None         # já armazenado sem máscara
    phone: Optional[str] = None
    birthdate: Optional[date] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = 'CLIENT'
    cpf: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None

    @validator('cpf', pre=True)
    def cpf_validate(cls, v):
        if v is None:
            return None
        normalized = normalize_cpf(v)
        if not normalized or not validate_cpf(normalized):
            raise ValueError("CPF inválido")
        return normalized

    @validator('phone', pre=True)
    def phone_validate(cls, v):
        if v is None:
            return None
        formatted = validate_and_format_phone(v)
        if formatted is None:
            raise ValueError("Telefone inválido")
        return formatted

    @validator('birthdate', pre=True)
    def birthdate_validate(cls, v):
        if v is None:
            return None
        if not validate_birthdate(v):
            raise ValueError("Data de nascimento inválida")
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None

    @validator('cpf', pre=True)
    def cpf_validate(cls, v):
        if v is None:
            return None
        normalized = normalize_cpf(v)
        if not normalized or not validate_cpf(normalized):
            raise ValueError("CPF inválido")
        return normalized

    @validator('phone', pre=True)
    def phone_validate(cls, v):
        if v is None:
            return None
        formatted = validate_and_format_phone(v)
        if formatted is None:
            raise ValueError("Telefone inválido")
        return formatted

    @validator('birthdate', pre=True)
    def birthdate_validate(cls, v):
        if v is None:
            return None
        if not validate_birthdate(v):
            raise ValueError("Data de nascimento inválida")
        return v

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
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserCreateModerator(BaseModel):
    """
    Schema para criação de um moderador.
    """
    name: str
    email: EmailStr
    password: str
    role: str = "MODERATOR"  # Define o papel padrão como MODERATOR