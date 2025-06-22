# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from app.db.models import UserRole # Importa o Enum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True # Permite que o Pydantic leia dados de objetos (ORM mode)