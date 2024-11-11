from fastapi import APIRouter
from src.schemas.user import UserCreate, UserUpdate, UserLogin
from src.controllers.auth_controller import register_user, login_user, update_user, logout_user, get_active_user, delete_user, get_info

router = APIRouter()

@router.post("/register", summary="Registrar usuario")
def register(user_create: UserCreate):
    return register_user(user_create)

@router.post("/login", summary="Login de usuario")
def login(login: UserLogin):
    return login_user(login.identifier, login.password)

@router.post("/logout", summary="Logout de usuario")
def logout():
    return logout_user()

@router.put("/update", summary="Actualizar información de usuario")
def update_user_info(user_update: UserUpdate):
    return update_user(user_update)

@router.get("/users", summary="Obtener todos los usuarios")
def get_users():
    return get_users()

@router.get("/info", summary="Obtener info del usuario")
def get_user_info():
    return get_info()

@router.get("/active", summary="Obtener usuario activo")
def get_active():
    return get_active_user()

@router.delete("/delete", summary="Eliminar usuario")
def delete():
    return delete_user()
