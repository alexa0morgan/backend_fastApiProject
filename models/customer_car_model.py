from dataclasses import dataclass
from typing import Literal

from fastapi import Query
from sqlmodel import SQLModel, Field, Relationship

from models.base_models import OrderBy, Pagination
from models.car_model import Car, CarResponse, CarResponseWithoutIds
from models.user_model import User, PartialUserResponse


class CustomerCarBase(SQLModel):
    car_id: int = Field(default=None, foreign_key="car.id")
    customer_id: int = Field(default=None, foreign_key="user.id")
    year: int
    license_plate: str


class CustomerCar(CustomerCarBase, table=True):
    __tablename__ = "customer_car"

    id: int = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    customer: User | None = Relationship(back_populates="customer_cars")
    car: Car | None = Relationship(back_populates="customer_cars")
    orders: list["Order"] = Relationship(back_populates="customer_car")


class CustomerCarCreate(CustomerCarBase):
    pass


class CustomerCarResponse(CustomerCarBase):
    id: int
    customer_id: int = Field(exclude=True)
    customer: PartialUserResponse | None = None
    car: CarResponse | None = None


class CustomerCarResponseWithoutIds(CustomerCarBase):
    id: int
    car_id: int = Field(exclude=True)
    customer_id: int = Field(exclude=True)
    customer: PartialUserResponse | None = None
    car: CarResponseWithoutIds | None = None


class CustomerCarUpdate(CustomerCarBase):
    year: int | None = None
    license_plate: str | None = None
    car_id: int | None = None
    customer_id: int | None = None


@dataclass
class CustomerCarQuery(Pagination, OrderBy):
    order_field: Literal['id', 'year', 'license_plate'] = Query("id")

    id: int | None = Query(None)
    id_in: list[int] = Query(None)
    car_id: int | None = Query(None)
    car_id_in: list[int] = Query(None)
    customer_id: int | None = Query(None)
    customer_id_in: list[int] = Query(None)
    year: int | None = Query(None)
    year_gt: int | None = Query(None)
    year_lt: int | None = Query(None)
    year_in: list[int] = Query(None)
    license_plate: str | None = Query(None)
    license_plate_in: list[str] = Query(None)
    customer_first_name: str | None = Query(None)
    customer_first_name_in: list[str] = Query(None)
    customer_last_name: str | None = Query(None)
    customer_last_name_in: list[str] = Query(None)
    car_model: str | None = Query(None)
    car_model_in: list[str] = Query(None)
