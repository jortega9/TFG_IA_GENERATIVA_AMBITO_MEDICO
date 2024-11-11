# backend/src/controllers/auth_controller.py

from fastapi import HTTPException
from src.schemas.user import User, UserCreate, UserUpdate
from src.services.auth_service import hash_password, verify_password, create_access_token
from datetime import timedelta
from db.database import DatabaseConnection
from datetime import datetime
import uuid

# Simulación de una base de datos en memoria
fake_users_db = {}
db = DatabaseConnection()

def unique_uuid_user():
    uuid_user = str(uuid.uuid4())
    return uuid_user


#ver como hacemos para ver si es medico group = 1 o admin group = 0
def register_user(user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    uuid = unique_uuid_user()
    user = User(
        uuid_user= uuid,
        name= user_create.name,
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
    try:
        user = db.get_user_identifier(identifier)
        if not user:
            print(f"No se encontró el usuario con el identificador: {identifier}")
            raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")

        if not verify_password(password, user["password"]):
            print(f"Contraseña incorrecta para el usuario: {identifier}")
            raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")

        access_token = create_access_token(data={"sub": user["email"]})
        db.update_user_login(user["uuid_user"], datetime.now(), access_token)
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        print(f"Error en login_user: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor durante el proceso de login")
    

def logout_user():
    try:
        db.update_user_logout(datetime.now())
        return {"user_id_logout": "logout"}
        
    except Exception as e:
        print(f"Error en login_user: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor durante el proceso de login")
    

def get_active_user():
    try:
        user = db.get_active_user()
        if user:
            return user

        return None
    except Exception as e:
        print("Error en get_active_user:", e)  # Agrega este print para más detalles
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
def get_info():
    try:
        info = db.get_user_info()
        return info
    except Exception as e:
        print("Error en get_active_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

def update_user(user_update: UserUpdate):
    try:
        user = db.update_user_account(user_update)
        return user
    except Exception as e:
        print("Error en update_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

def delete_user():
    try:
        db.delete_user()
    except Exception as e:
        print("Error en get_active_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
