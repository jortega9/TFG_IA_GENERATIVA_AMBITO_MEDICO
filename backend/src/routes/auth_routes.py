from fastapi import APIRouter, Depends
from src.schemas.user import UserCreate, UserUpdate, UserLogin, UserIdentifier, PwdUpdate, PatientCreate, UpdatePatient
from src.controllers.auth_controller import register_user, login_user, update_user, logout_user, get_active_user, delete_user, get_info, get_exist_user, update_pwd, add_newPatient, update_patientName, get_patients, delete_patient
from src.services.auth_service import get_current_user


router = APIRouter()

@router.post("/register", summary="Registrar usuario")
def register(user_create: UserCreate):
    return register_user(user_create)

@router.post("/user-exist", summary="Verificar si el usuario existe")
def user_exist(user: UserIdentifier):
    return get_exist_user(user.identifier)

@router.post("/login", summary="Login de usuario")
def login(login: UserLogin):
    return login_user(login.identifier, login.password)

@router.post("/logout", summary="Logout de usuario")
def logout(current_user: dict = Depends(get_current_user)):
    uuid = current_user["uuid"]
    return logout_user(uuid)

@router.put("/update", summary="Actualizar información de usuario")
def update_user_info(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    uuid = current_user["uuid"]
    return update_user(user_update, uuid)

@router.put("/updatePwd", summary="Actualizar contraseña de usuario")
def update_user_pwd(pwd_update: PwdUpdate, current_user: dict = Depends(get_current_user)):
    uuid = current_user["uuid"]
    return update_pwd(pwd_update, uuid)

@router.get("/users", summary="Obtener todos los usuarios")
def get_users():
    return get_users()

@router.get("/info", summary="Obtener info del usuario")
def get_user_info(current_user: dict = Depends(get_current_user)):
    uuid = current_user["uuid"]
    return get_info(uuid)

@router.get("/active", summary="Obtener usuario activo")
def get_active(current_user: dict = Depends(get_current_user)):
    uuid = current_user["uuid"]
    print(uuid)
    return get_active_user(uuid)

@router.delete("/delete", summary="Eliminar usuario")
def delete(current_user: dict = Depends(get_current_user)):
    uuid = current_user["uuid"]
    return delete_user(uuid)

#---------------------Patients-----------------------------

@router.post("/newPatient", summary="Nuevo paciente")
def newPatient(patient_create: PatientCreate):
    return add_newPatient(patient_create)

@router.post("/updatePatient", summary="Actualizar nombre paciente")
def updateName(updatePatient: UpdatePatient):
    return update_patientName(updatePatient)

@router.get("/patients", summary="Obtener todos los pacientes")
def get_patientsInfo():
    return get_patients()

@router.delete("/delete/{id}", summary="Eliminar paciente")
def deletePatient(id: str):
    return delete_patient(id)