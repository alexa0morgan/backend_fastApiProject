from typing import TypeVar, Type, Any, Sequence

from sqlmodel import SQLModel, Session, select

from models.base_models import Pagination, OrderBy

TT = TypeVar("TT", bound=Type[SQLModel])
T = TypeVar("T", bound=SQLModel)


def get_all(session: Session, cls: TT, options: list[Any], pagination_and_ordering: Pagination | OrderBy,
            joins: list[SQLModel] | None = None) -> Sequence[T]:
    query = select(cls)

    if joins:
        for join in joins:
            query = query.join(join)

    return session.exec(
        query
        .where(*options)
        .order_by(pagination_and_ordering.get_order_by(cls))
        .offset(pagination_and_ordering.offset)
        .limit(pagination_and_ordering.limit)
    ).all()
