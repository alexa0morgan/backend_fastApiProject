from dataclasses import dataclass
from typing import Literal

from fastapi import Query
from pydantic import BaseModel, computed_field
from sqlmodel import SQLModel, Field, Relationship

from models.base_models import OrderBy, Pagination
from models.service_order_model import ServiceOrder


class Price(BaseModel):
    cents: int
    rubles: int
    formatted: str


class Time(BaseModel):
    seconds: int
    minutes: int


class ServiceBase(SQLModel):
    name: str
    minPrice: int = Field(description="Price in cents")
    minTime: int = Field(description="Time in seconds")


class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    orders: list["Order"] = Relationship(back_populates="services", link_model=ServiceOrder)


class ServiceCreate(ServiceBase):
    pass


class ServiceResponse(ServiceBase):
    id: int
    minPrice: int = Field(exclude=True)
    minTime: int = Field(exclude=True)

    @computed_field(return_type=Price)
    @property
    def price(self):
        return Price(
            cents=self.minPrice,
            rubles=self.minPrice // 100,
            formatted=f"{self.minPrice // 100} руб. {self.minPrice % 100} коп."
        )

    @computed_field(return_type=Time)
    @property
    def time(self):
        return Time(
            seconds=self.minTime,
            minutes=self.minTime // 60
        )


class ServiceUpdate(ServiceBase):
    name: str | None = None
    minPrice: int | None = None
    minTime: int | None = None


@dataclass
class ServiceQuery(Pagination, OrderBy):
    order_field: Literal['id', 'name', 'minPrice', 'minTime'] = Query("id")

    id: int | None = Query(None)
    id_in: list[int] = Query(None)
    name: str | None = Query(None)
    name_in: list[str] = Query(None)
    price: int | None = Query(None)
    price_gt: int | None = Query(None)
    price_lt: int | None = Query(None)
    price_in: list[int] = Query(None)
    time: int | None = Query(None)
    time_gt: int | None = Query(None)
    time_lt: int | None = Query(None)
    time_in: list[int] = Query(None)
