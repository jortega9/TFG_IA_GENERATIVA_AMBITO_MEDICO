from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    uuid_user: str
    username: str
    email: EmailStr
    password: str
    secret: str
    date: datetime
    last_update: datetime
    last_login: datetime
    uuid_group: str
    validated: int
    token: str
    is_active: int

class UserLogin(BaseModel):
    identifier: str
    password: str

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
