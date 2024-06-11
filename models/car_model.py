from dataclasses import dataclass
from typing import Literal

from fastapi import Query
from pydantic import computed_field
from sqlmodel import Field, SQLModel, Relationship

from models.base_models import OrderBy, Pagination
from models.brand_model import Brand, BrandResponse


class CarBase(SQLModel):
    model: str

    brand_id: int | None = Field(default=None, foreign_key="brand.id")


class Car(CarBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    brand: Brand | None = Relationship(back_populates="cars")
    customer_cars: list["CustomerCar"] = Relationship(back_populates="car")


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    brand_id: int = Field(exclude=True)
    brand: BrandResponse | None = None


class CarResponseWithoutIds(CarBase):
    brand_id: int = Field(exclude=True)
    brand: BrandResponse | None = Field(exclude=True)

    @computed_field(return_type=str)
    @property
    def brand_name(self):
        return self.brand.name


class CarUpdate(CarBase):
    model: str | None = None
    brand_id: int | None = None


@dataclass
class CarQuery(Pagination, OrderBy):
    order_field: Literal['id', 'model', 'brand_id'] = Query("id")

    id: int | None = Query(None)
    id_in: list[int] = Query(None)
    model: str | None = Query(None)
    model_in: list[str] = Query(None)
    brand_id: int | None = Query(None)
    brand_id_in: list[int] = Query(None)
    brand_name: str | None = Query(None)
    brand_name_in: list[str] = Query(None)
