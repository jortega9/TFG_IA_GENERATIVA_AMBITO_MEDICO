# backend/src/controllers/auth_controller.py

from fastapi import HTTPException
from src.schemas.user import User, UserCreate, UserUpdate
from src.services.auth_service import hash_password, verify_password, create_access_token
from datetime import timedelta

# Simulación de una base de datos en memoria
fake_users_db = {}

def register_user(user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    user = User(
        id=len(fake_users_db) + 1,
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password,
        is_active=True
    )
    fake_users_db[user.email] = user
    return user

def login_user(email: str, password: str):
    user = fake_users_db.get(email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

def update_user(email: str, user_update: UserUpdate):
    user = fake_users_db.get(email)
    if user:
        user.username = user_update.username or user.username
        user.email = user_update.email or user.email
        if user_update.password:
            user.hashed_password = hash_password(user_update.password)
        return user
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

def deactivate_user(email: str):
    user = fake_users_db.get(email)
    if user:
        user.is_active = False
        return {"msg": "Usuario desactivado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
