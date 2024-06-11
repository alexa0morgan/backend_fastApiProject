from dataclasses import dataclass
from typing import Literal, Type

from fastapi import Query


@dataclass
class Pagination:
    offset: int | None = Query(0)
    limit: int | None = Query(5, le=100)


@dataclass
class OrderBy:
    order_field: str = Query(None)
    order_direction: Literal["asc", "desc"] = Query("asc")

    def get_order_by(self, cls: Type):
        order = getattr(cls, self.order_field)
        return order if self.order_direction == 'asc' else order.desc()
