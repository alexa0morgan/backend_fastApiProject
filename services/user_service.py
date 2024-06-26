from fastapi import HTTPException, status
from sqlmodel import select

from models.user_model import User, UserCreate, UserQuery
from services.auth_service import AuthService
from services.base_service import BaseService


class UserService(BaseService):
    cls = User

    def email_exists(self, email: str) -> bool:
        return self.session.exec(select(User).where(User.email == email)).first() is not None

    def create(self, user: UserCreate) -> User:
        if self.email_exists(user.email):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"User with this email already exists"
            )

        db_user = User.model_validate(
            user,
            update={
                "hashed_password": AuthService.hash_password(user.password)
            }
        )
        return self.save_and_refresh(db_user)

    def read(self, query: UserQuery):
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

        return self.get_all(options, query)

    def update(self, user_id: int, user):
        db_user = self.get_one(user_id)
        user_data = user.model_dump(exclude_unset=True)
        if "password" in user_data:
            user_data["hashed_password"] = AuthService.hash_password(user_data["password"])
            del user_data["password"]
        db_user.sqlmodel_update(user_data)
        return self.save_and_refresh(db_user)
