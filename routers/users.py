from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from db import engine
from models.user import UserResponse, User, UserCreate, UserUpdate
from routers.auth import CurrentUser, pwd_context, CurrentAdminUser

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: CurrentUser):
    return current_user


@router.post("/create", response_model=UserResponse)
def create_user(user: UserCreate, _: CurrentAdminUser):
    hashed_password = pwd_context.hash(user.password)
    with Session(engine) as session:
        extra_data = {"hashed_password": hashed_password}
        db_user = User.model_validate(user, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@router.patch("/update/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, _: CurrentAdminUser):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
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
def delete_user(user_id: int, _: CurrentAdminUser):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.deleted_at = datetime.now()
        session.commit()
        return {"message": "User deleted successfully"}
