from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from db import engine
from models.user import UserResponse, User, UserCreate, UserUpdate, Role
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


@router.get("/", response_model=list[UserResponse])
def read_users(_: CurrentAdminUser,

               user_id: int = Query(None),
               user_ids: list[int] = Query(None),
               first_name: str = Query(None),
               first_names: list[str] = Query(None),
               last_name: str = Query(None),
               last_names: list[str] = Query(None),
               patronymic: str = Query(None),
               patronymics: list[str] = Query(None),
               email: str = Query(None),
               emails: list[str] = Query(None),
               role_id: Role = Query(None),
               role_ids: list[Role] = Query(None),
               send_notifications: bool = Query(None),

               offset: int = Query(0),
               limit: int = Query(default=5, le=100)):
    with (Session(engine) as session):
        user = session.exec(select(User)
                            .where(User.id == user_id if user_id else True)
                            .where(User.id.in_(user_ids) if user_ids else True)
                            .where(User.first_name.like(f"%{first_name}%") if first_name else True)
                            .where(User.first_name.in_(first_names) if first_names else True)
                            .where(User.last_name.like(f"%{last_name}%") if last_name else True)
                            .where(User.last_name.in_(last_names) if last_names else True)
                            .where(User.patronymic.like(f"%{patronymic}%") if patronymic else True)
                            .where(User.patronymic.in_(patronymics) if patronymics else True)
                            .where(User.email.like(f"%{email}%") if email else True)
                            .where(User.email.in_(emails) if emails else True)
                            .where(User.role_id == role_id if role_id else True)
                            .where(User.role_id.in_(role_ids) if role_ids else True)
                            .where(User.send_notifications == send_notifications if send_notifications else True)

                            .offset(offset)
                            .limit(limit)
                            .order_by(User.id)  # обратная сортировка User.id.desc()
                            ).all()
        return user


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
        db_user.deleted_at = str(datetime.now(timezone.utc)) + 'Z'
        session.commit()
        return {"message": "User deleted successfully"}
