from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None

class UserRead(UserBase):
    id: UUID
    role: str
    access: list[str] = []
    is_active: bool
    is_2fa_enabled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    role: str = "User"
    access: list[str] = []
    is_active: bool = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    role: Optional[str] = None
    access: Optional[list[str]] = None
    is_active: Optional[bool] = None
