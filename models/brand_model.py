from dataclasses import dataclass
from typing import Literal

from fastapi import Query
from sqlmodel import Field, SQLModel, Relationship

from models.base_models import OrderBy, Pagination


class BrandBase(SQLModel):
    name: str


class Brand(BrandBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    cars: list["Car"] = Relationship(back_populates="brand")


class BrandCreate(BrandBase):
    pass


class BrandResponse(BrandBase):
    id: int


class BrandUpdate(BrandBase):
    name: str | None = None


@dataclass
class BrandQuery(Pagination, OrderBy):
    order_field: Literal['id', 'name'] = Query('id')

    id: int | None = Query(None)
    id_in: list[int] = Query(None)
    name: str | None = Query(None)
    name_in: list[str] = Query(None)
