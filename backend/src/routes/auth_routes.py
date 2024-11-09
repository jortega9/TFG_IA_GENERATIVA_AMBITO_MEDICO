from fastapi import APIRouter
from src.schemas.user import UserCreate, UserUpdate, UserLogin
from src.controllers.auth_controller import register_user, login_user, update_user, deactivate_user

router = APIRouter()

@router.post("/register", summary="Registrar usuario")
def register(user_create: UserCreate):
    return register_user(user_create)

@router.post("/login", summary="Login de usuario")
def login(login: UserLogin):
    return login_user(login.identifier, login.password)

@router.put("/update", summary="Actualizar información de usuario")
def update_user_info(identifier: str, user_update: UserUpdate):
    return update_user(identifier, user_update)

@router.delete("/deactivate", summary="Desactivar usuario")
def deactivate_user_account(identifier: str):
    return deactivate_user(identifier)

@router.get("/users", summary="Obtener todos los usuarios")
def get_users():
    return get_users()

#eliminar user
@router.delete("/delete", summary="Eliminar usuario")
def delete_user(identifier: str):
    return delete_user(identifier)
