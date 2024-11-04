# backend/src/controllers/auth_controller.py

from fastapi import HTTPException
from src.schemas.user import User, UserCreate, UserUpdate
from src.services.auth_service import hash_password, verify_password, create_access_token
from datetime import timedelta
from db.database import DatabaseConnection
from pydantic import BaseModel
from datetime import datetime
import uuid

# Simulación de una base de datos en memoria
fake_users_db = {}
db = DatabaseConnection()

class User(BaseModel):
    uuid_user: str
    username: str
    email: str
    password: str
    secret: str
    date: datetime
    last_update: datetime
    last_login: datetime
    uuid_group: str
    validated: int
    token: str
    is_active: int

def unique_uuid_user():
    uuid_user = str(uuid.uuid4())
    return uuid_user


#ver como hacemos para ver si es medico group = 1 o admin group = 0
def register_user(user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    uuid = unique_uuid_user()
    user = User(
        uuid_user= uuid,
        username= user_create.name[0:3] + uuid[0:5],
        email= user_create.email,
        password= hashed_password,
        secret= hashed_password,
        date= datetime.now(),
        last_update= datetime.now(),
        last_login= datetime.now(),
        uuid_group= 0,
        validated= 0,
        token= "",
        is_active=True,
    )

    try:
        db.insert_user(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def login_user(identifier: str, password: str):
    user = db.get_user_identifier(identifier)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def update_user(identifier: str, user_update: UserUpdate):
    user = db.get_user_identifier(identifier)
    if user:
        user.username = user_update.username or user.username
        user.email = user_update.email or user.email
        if user_update.password:
            user.password = hash_password(user_update.password)
        return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def deactivate_user(identifier: str):
    user = db.get_user_identifier(identifier)
    if user:
        user.is_active = False
        return {"msg": "Usuario desactivado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def delete_user(identifier: str):
    user = db.get_user_identifier(identifier)
    if user:
        db.delete_user(user.uuid_user)
        return {"msg": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
