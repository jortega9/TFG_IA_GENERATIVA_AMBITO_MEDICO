from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    """TODO: Cambiar a una UUID"""
    name: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True

class UserCreate(BaseModel):
    """Data that user needs to register in the database."""
    
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Data that user can change and update in the database."""
    
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
