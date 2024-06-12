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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "97bcf47e14474a6fab00cda51846e7d0fa2da14f653846699165981341222248"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService(BaseService):
    def authenticate_user(self, username: str, password: str):
        user = self.session.exec(
            select(User)
            .where(User.email == username)
        ).first()
        if user.deleted_at:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or deleted")
        if not user:
            return False
        if not pwd_context.verify(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_current_user(session: CurrentSession, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

    CurrentUser = Annotated[User, Depends(get_current_user)]

    @staticmethod
    def current_user_as_admin(current_user: CurrentUser):
        if current_user.role_id != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not an admin")
        return current_user

    CurrentAdminUser = Annotated[User, Depends(current_user_as_admin)]

    def login(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
