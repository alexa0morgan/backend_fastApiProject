from datetime import timedelta, datetime, UTC
from typing import Annotated

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import select

from db import CurrentSession
from models.auth_model import TokenData, Token
from models.user_model import User, Role
from services.base_service import BaseService
from dotenv import load_dotenv
import os

load_dotenv()

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_SECRET_KEY = os.getenv("SECRET_KEY")
_ALGORITHM = os.getenv("ALGORITHM")
_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class AuthService(BaseService):
    def _authenticate_user(self, username: str, password: str):
        user = self.session.exec(
            select(User)
            .where(User.email == username)
        ).first()
        if user.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or deleted")
        if not user:
            return False
        if not AuthService.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return _pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password: str):
        return _pwd_context.hash(password)

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, _SECRET_KEY, algorithm=_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def _get_current_user(session: CurrentSession, token: Annotated[str, Depends(_oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, _SECRET_KEY, algorithms=[_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception

        user = session.exec(
            select(User)
            .where(User.email == token_data.username)
            .where(User.deleted_at == None)
        ).first()
        if user is None:
            raise credentials_exception
        return user

    CurrentUser = Annotated[User, Depends(_get_current_user)]

    @staticmethod
    def _current_user_as_admin(current_user: CurrentUser):
        if current_user.role_id != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")
        return current_user

    CurrentAdminUser = Annotated[User, Depends(_current_user_as_admin)]

    def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = self._authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService._create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
