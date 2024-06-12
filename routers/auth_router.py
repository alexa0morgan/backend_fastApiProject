from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.auth_model import Token
from services.auth_service import AuthService

router = APIRouter()


@router.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: AuthService = Depends()
) -> Token:
    return auth_service.login(form_data)
