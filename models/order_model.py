import enum
from dataclasses import dataclass
from typing import Literal

from fastapi import Query
from pydantic import computed_field, BaseModel
from sqlmodel import SQLModel, Field, Column, Enum, Relationship

from models.base_models import OrderBy, Pagination
from models.customer_car_model import CustomerCar, CustomerCarResponseWithoutIds
from models.service_model import ServiceResponse
from models.service_order_model import ServiceOrder
from models.user_model import User, PartialUserResponse


class Status(int, enum.Enum):
    in_progress = 1
    completed = 2


class OrderBase(SQLModel):
    administrator_id: int = Field(default=None, foreign_key="user.id")
    employee_id: int = Field(default=None, foreign_key="user.id")
    customer_car_id: int = Field(default=None, foreign_key="customer_car.id")


class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)
    start_date: str
    end_date: str | None
    status: Status = Field(default=Status.in_progress, sa_column=Column(Enum(Status)))
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
    services: list["Service"] = Relationship(back_populates="orders", link_model=ServiceOrder)


class OrderCreate(OrderBase):
    services: list[int]


class OrderResponse(OrderBase):
    id: int
    customer_car: CustomerCarResponseWithoutIds | None = None
    administrator: PartialUserResponse | None = None
    employee: PartialUserResponse | None = None
    start_date: str
    end_date: str | None
    status: Status = Field(default=Status.in_progress, sa_column=Column(Enum(Status)))
    administrator_id: int = Field(exclude=True)
    employee_id: int = Field(exclude=True)
    customer_car_id: int = Field(exclude=True)

    services: list["ServiceResponse"]

    @computed_field(return_type=int)
    @property
    def total_price(self):
        return sum([service.minPrice for service in self.services]) // 100

    @computed_field(return_type=int)
    @property
    def total_time(self):
        return sum([service.minTime for service in self.services]) // 60


class OrderUpdate(OrderBase):
    end_date: str | None

    administrator_id: int | None = None
    employee_id: int | None = None
    customer_car_id: int | None = None


class OrderAddServices(BaseModel):
    service_ids: list[int]


@dataclass
class OrderQuery(Pagination, OrderBy):
    order_field: Literal['id', 'start_date', 'end_date', 'status'] = Query("id")

    id: int | None = Query(None)
    id_in: list[int] = Query(None)
    customer_car_id: int | None = Query(None)
    customer_car_id_in: list[int] = Query(None)
    customer_car_year: int | None = Query(None)
    customer_car_year_gt: int | None = Query(None)
    customer_car_year_lt: int | None = Query(None)
    customer_car_license_plate: str | None = Query(None)
    customer_id: int | None = Query(None)
    customer_id_in: list[int] = Query(None)
    administrator_id: int | None = Query(None)
    administrator_id_in: list[int] = Query(None)
    employee_id: int | None = Query(None)
    employee_id_in: list[int] = Query(None)
    status: Status = Query(None)
    start_date_gte: str | None = Query(None)
    start_date_lte: str | None = Query(None)
    end_date_gte: str | None = Query(None)
    end_date_lte: str | None = Query(None)
