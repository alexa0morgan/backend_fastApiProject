from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException, Depends, status

from db import CurrentSession
from models.user_model import UserResponse, User, UserCreate, UserUpdate, UserQuery
from routers.auth_router import CurrentUser, pwd_context, CurrentAdminUser
from services.base_service import get_all

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: CurrentUser):
    return current_user


@router.post("/create", response_model=UserResponse)
def create_user(
        session: CurrentSession,
        _: CurrentAdminUser,
        user: UserCreate
):
    db_user = User.model_validate(
        user,
        update={
            "hashed_password": pwd_context.hash(user.password)
        }
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserResponse])
def read_users(
        session: CurrentSession,
        _: CurrentAdminUser,
        query: UserQuery = Depends()
):
    options = [User.deleted_at == None]

    if query.id:
        options.append(User.id == query.id)
    if query.id_in:
        options.append(User.id.in_(query.id_in))
    if query.email:
        options.append(User.email.ilike(f'%{query.email}%'))
    if query.role_id:
        options.append(User.role_id == query.role_id)
    if query.role_id_in:
        options.append(User.role_id.in_(query.role_id_in))
    if query.send_notifications is not None:
        options.append(User.send_notifications == query.send_notifications)
    if query.first_name:
        options.append(User.first_name.ilike(f'%{query.first_name}%'))
    if query.first_name_in:
        options.append(User.first_name.in_(query.first_name_in))
    if query.last_name:
        options.append(User.last_name.ilike(f'%{query.last_name}%'))
    if query.last_name_in:
        options.append(User.last_name.in_(query.last_name_in))
    if query.patronymic:
        options.append(User.patronymic.ilike(f'%{query.patronymic}%'))
    if query.patronymic_in:
        options.append(User.patronymic.in_(query.patronymic_in))

    return get_all(session, User, options, query)


@router.patch("/update/{user_id}", response_model=UserResponse)
def update_user(
        session: CurrentSession,
        _: CurrentAdminUser,
        user_id: int,
        user: UserUpdate,
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["hashed_password"] = pwd_context.hash(user_data["password"])
        del user_data["password"]
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/delete/{user_id}")
def delete_user(
        session: CurrentSession,
        _: CurrentAdminUser,
        user_id: int,
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.deleted_at = datetime.now(UTC).isoformat()
    session.commit()
    return {"message": "User deleted successfully"}
