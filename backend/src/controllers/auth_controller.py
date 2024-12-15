# backend/src/controllers/auth_controller.py

from fastapi import HTTPException
from src.schemas.user import User, UserCreate, UserUpdate, PwdUpdate, PatientCreate, UpdatePatient
from src.services.auth_service import hash_password, verify_password, create_access_token, get_current_user
from datetime import timedelta
from db.database import DatabaseConnection
from datetime import datetime
import uuid
import random

# Simulación de una base de datos en memoria
fake_users_db = {}
db = DatabaseConnection()

def unique_uuid_user():
    uuid_user = str(uuid.uuid4())
    return uuid_user

def register_user(user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    uuid = unique_uuid_user()
    user = User(
        uuid_user= uuid,
        name= user_create.name,
        username= user_create.name[0:3] + str(random.randint(100, 999)),
        email= user_create.email,
        password= hashed_password,
        secret= None,
        date= datetime.now(),
        last_update= datetime.now(),
        last_login= datetime.now(),
        uuid_group= "12345",
        validated= 0,
        token= None,
        is_active=False,
    )

    try:
        db.insert_user(user)
        return user
    except Exception as e:
        print(f"Error en register_user: {e}")
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

        access_token = create_access_token(data={"sub": user["uuid_user"]})
        db.update_user_login(user["uuid_user"], datetime.now(), access_token)
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        print(f"Error en login_user: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor durante el proceso de login")
    

def logout_user(uuid: str):
    try:
        db.update_user_logout(uuid, datetime.now())
        return {"user_id_logout": "logout"}
        
    except Exception as e:
        print(f"Error en login_user: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor durante el proceso de login")
    

def get_active_user(uuid: str):
    try:
        user = db.get_active_user(uuid)
        if user:
            return user

        return None
    except Exception as e:
        print("Error en get_active_user:", e)  # Agrega este print para más detalles
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
def get_exist_user(identifier: str):
    try:
        exist = db.get_user_exist(identifier)
        return {"user_exists": exist}
    except Exception as e:
        print("Error en get_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    
def get_info(uuid: str):
    try:
        info = db.get_user_info(uuid)
        return info
    except Exception as e:
        print("Error en get_active_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

def update_user(user_update: UserUpdate, uuid: str):
    try:
        user = db.update_user_account(user_update, uuid)
        return user
    except Exception as e:
        print("Error en update_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
def update_pwd(pwd_update: PwdUpdate, uuid: str):
    try:
        hashed_password = hash_password(pwd_update.password)
        user = db.update_user_pwd(hashed_password, pwd_update.email, uuid)
        return user
    except Exception as e:
        print("Error en update_pwd:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")

def delete_user(uuid: str):
    try:
        db.delete_user(uuid)
    except Exception as e:
        print("Error en get_active_user:", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
# ----------------------- Patients ------------------------------------

def add_newPatient(patient: PatientCreate):

    try:
        db.insert_patient(patient)
        return patient
    except Exception as e:
        print(f"Error en register_user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def update_patientName(updatePatient: UpdatePatient):

    try:
        db.update_patient(updatePatient.id, updatePatient.newName)
        return updatePatient.newName
    except Exception as e:
        print(f"Error en register_user: {e}")
        raise HTTPException(status_code=500, detail=str(e))