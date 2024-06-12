from fastapi import APIRouter, Depends

from models.user_model import UserResponse, UserCreate, UserUpdate, UserQuery
from services.auth_service import AuthService
from services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: AuthService.CurrentUser):
    return current_user


@router.post("/create", response_model=UserResponse)
def create_user(
        _: AuthService.CurrentAdminUser,
        user: UserCreate,
        user_service: UserService = Depends()
):
    return user_service.create(user)


@router.get("/", response_model=list[UserResponse])
def read_users(
        _: AuthService.CurrentAdminUser,
        query: UserQuery = Depends(),
        user_service: UserService = Depends()
):
    return user_service.read(query)


@router.patch("/update/{user_id}", response_model=UserResponse)
def update_user(
        _: AuthService.CurrentAdminUser,
        user_id: int,
        user: UserUpdate,
        user_service: UserService = Depends()
):
    return user_service.update(user_id, user)


@router.delete("/delete/{user_id}")
def delete_user(
        _: AuthService.CurrentAdminUser,
        user_id: int,
        user_service: UserService = Depends()
):
    return user_service.delete(user_id)
