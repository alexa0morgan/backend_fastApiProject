from datetime import datetime, UTC
from typing import TypeVar, Type, Any, Sequence

from fastapi import HTTPException, status
from sqlmodel import SQLModel, select

from db import CurrentSession
from models.base_models import Pagination, OrderBy

TTypeModel = TypeVar("TTypeModel", bound=Type[SQLModel])
TModel = TypeVar("TModel", bound=SQLModel)


class BaseService:
    cls: TTypeModel

    def __init__(self, session: CurrentSession):
        self.session = session

    def get_one(self, cls: TTypeModel, id: int):
        db_obj = self.session.get(cls, id)

        if not db_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__} not found")

        return db_obj

    def get_all(self, cls: TTypeModel, options: list[Any], pagination_and_ordering: Pagination | OrderBy,
                joins: list | None = None) -> Sequence[TModel]:
        query = select(cls)

        if joins:
            for join in joins:
                query = query.join(join)

        return self.session.exec(
            query
            .where(*options)
            .order_by(pagination_and_ordering.get_order_by(cls))
            .offset(pagination_and_ordering.offset)
            .limit(pagination_and_ordering.limit)
        ).all()

    def mark_deleted(self, db_obj: TModel):
        db_obj.deleted_at = datetime.now(UTC).isoformat()
        self.session.commit()

    def save_and_refresh(self, obj: TModel) -> TModel:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def create(self, create_data) -> TTypeModel:
        db_obj = self.cls.model_validate(create_data)
        return self.save_and_refresh(db_obj)

    def update(self, id: int, update_data):
        db_obj = self.get_one(self.cls, id)
        obj_data = update_data.model_dump(exclude_unset=True)
        db_obj.sqlmodel_update(obj_data)
        return self.save_and_refresh(db_obj)

    def delete(self, id: int):
        db_obj = self.get_one(self.cls, id)

        self.mark_deleted(db_obj)
        return {"message": f"{self.cls.__name__} deleted successfully"}


def get_all(session, cls: TTypeModel, options: list[Any], pagination_and_ordering: Pagination | OrderBy,
            joins: list | None = None) -> Sequence[TModel]:
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
