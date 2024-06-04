import enum

from sqlmodel import Field, SQLModel, Enum, Column


class Role(enum.Enum):
    admin = 1
    employee = 2
    client = 3


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    patronymic: str | None = None
    email: str
    role_id: Role = Field(sa_column=Column(Enum(Role)))
    send_notifications: bool


class UserInDB(User):
    hashed_password: str
