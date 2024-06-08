import enum

from sqlmodel import SQLModel, Field, Column, Enum, Relationship

from models.customer_car import CustomerCar
from models.user import User


class Status(enum.Enum):
    in_progress = 1
    completed = 2


class OrderBase(SQLModel):
    administrator_id: int = Field(default=None, foreign_key="user.id")
    employee_id: int = Field(default=None, foreign_key="user.id")
    customer_car_id: int = Field(default=None, foreign_key="customer_car.id")
    status: Status = Field(sa_column=Column(Enum(Status)))
    start_date: str
    end_date: str | None


class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    customer_car: CustomerCar | None = Relationship(back_populates="orders")
    administrator: User | None = Relationship(
        back_populates="administrator_orders",
        sa_relationship_kwargs={"foreign_keys": "Order.administrator_id"}
    )
    employee: User | None = Relationship(
        back_populates="employee_orders",
        sa_relationship_kwargs={"foreign_keys": "Order.employee_id"}
    )
