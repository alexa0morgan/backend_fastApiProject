import enum

from sqlmodel import Field, SQLModel, Enum, Column
from pydantic import computed_field, BaseModel


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


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    deleted_at: str | None = None


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


class PartialUserResponse(BaseModel):
    id: int
    email: str

    first_name: str = Field(exclude=True)
    last_name: str = Field(exclude=True)
    patronymic: str | None = Field(exclude=True)

    @computed_field(return_type=str)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.patronymic or ''}".strip()
