from sqlmodel import SQLModel, Field


class ServiceOrder(SQLModel, table=True):
    order_id: int | None = Field(default=None, foreign_key="order.id", primary_key=True)
    service_id: int | None = Field(default=None, foreign_key="service.id", primary_key=True)
