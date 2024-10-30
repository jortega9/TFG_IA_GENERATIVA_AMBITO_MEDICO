from fastapi import APIRouter
from src.schemas.user import UserCreate, UserUpdate
from src.controllers.auth_controller import register_user, login_user, update_user, deactivate_user

router = APIRouter()

@router.post("/register", summary="Registrar usuario")
def register(user_create: UserCreate):
    return register_user(user_create)

@router.post("/login", summary="Login de usuario")
def login(email: str, password: str):
    return login_user(email, password)

@router.put("/update", summary="Actualizar información de usuario")
def update_user_info(email: str, user_update: UserUpdate):
    return update_user(email, user_update)

@router.delete("/deactivate", summary="Desactivar usuario")
def deactivate_user_account(email: str):
    return deactivate_user(email)
