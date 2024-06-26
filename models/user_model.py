import enum
from dataclasses import dataclass
from typing import Literal

from fastapi import Query
from pydantic import computed_field, BaseModel
from sqlmodel import Field, SQLModel, Enum, Column, Relationship

from models.base_models import Pagination, OrderBy


class Role(int, enum.Enum):
    admin = 1
    employee = 2
    customer = 3


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

    customer_cars: list["CustomerCar"] = Relationship(back_populates="customer")

    administrator_orders: list["Order"] = Relationship(back_populates="administrator", sa_relationship_kwargs={
        "foreign_keys": "[Order.administrator_id]"})
    employee_orders: list["Order"] = Relationship(back_populates="employee",
                                                  sa_relationship_kwargs={"foreign_keys": "[Order.employee_id]"})


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


@dataclass
class UserQuery(Pagination, OrderBy):
    order_field: Literal['id', 'first_name', 'last_name', 'patronymic', 'email', 'role_id'] = Query("id")

    id: int | None = Query(None)
    id_in: list[int] = Query(None)
    first_name: str | None = Query(None)
    first_name_in: list[str] = Query(None)
    last_name: str | None = Query(None)
    last_name_in: list[str] = Query(None)
    patronymic: str | None = Query(None)
    patronymic_in: list[str] = Query(None)
    email: str | None = Query(None)
    email_in: list[str] = Query(None)
    role_id: Role = Query(None)
    role_id_in: list[Role] = Query(None)
    send_notifications: bool = Query(None)
