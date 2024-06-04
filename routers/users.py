from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import User, Role, UserInDB

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "johndoe": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "send_notifications": True,
        "hashed_password": "fakehashedsecret",
        "role_id": Role.admin,
    },
    "alice": {
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice@example.com",
        "send_notifications": True,
        "hashed_password": "fakehashedsecret",
        "role_id": Role.employee,
    },
    "bob": {
        "first_name": "Bob",
        "last_name": "Doe",
        "email": "bob@example.com",
        "send_notifications": False,
        "hashed_password": "fakehashedsecret",
        "role_id": Role.client,
    }
}


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user_dict['hashed_password']:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict['email'], "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
