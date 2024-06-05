import datetime
import enum

from sqlmodel import Field, SQLModel, Enum, Column


class Role(enum.Enum):
    admin = 1
    employee = 2
    client = 3


class UserBase(SQLModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: str = Field(unique=True)
    role_id: Role = Field(sa_column=Column(Enum(Role)))
    send_notifications: bool
    deleted_at: datetime.datetime | None = None


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserResponse(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    email: str | None = None
    role_id: Role | None = None
    send_notifications: bool | None = None
    password: str | None = None
