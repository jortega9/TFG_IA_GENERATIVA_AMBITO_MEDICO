from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    uuid_user: str
    name: str
    username: str
    email: EmailStr
    password: str
    secret: Optional[str]
    date: datetime
    last_update: datetime
    last_login: datetime
    uuid_group: str
    validated: int
    token: Optional[str]
    is_active: int

class UserLogin(BaseModel):
    identifier: str
    password: str

class UserIdentifier(BaseModel):
    identifier: str

class UserCreate(BaseModel):
    """Data that user needs to register in the database."""
    
    name: str
    email: EmailStr
    password: str

class PatientCreate(BaseModel):
    """Data that patients need to be added in the database."""
    
    name: str
    email: EmailStr
    phone: str
    gender: str
    age: int
    diseases: Optional[str] = None
    allergy: Optional[str] = None
    history: Optional[str] = None

class UserUpdate(BaseModel):
    """Data that user can change and update in the database."""
    
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class PwdUpdate(BaseModel):
    """Data that user can change and update in the database."""
    
    email: Optional[str] = None
    password: Optional[str] = None

class UpdatePatient(BaseModel):
    """Data that user can change and update in the database."""
    id: int
    newName: str
