from sqlmodel import SQLModel, Field, Relationship

from models.car import Car, CarResponse
from models.user import User, PartialUserResponse


class CustomerCarBase(SQLModel):
    car_id: int = Field(default=None, foreign_key="car.id")
    customer_id: int = Field(default=None, foreign_key="user.id")
    year: int
    license_plate: str


class CustomerCar(CustomerCarBase, table=True):
    id: int = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    customer: User | None = Relationship(back_populates="customer_cars")
    car: Car | None = Relationship(back_populates="customer_cars")


class CustomerCarCreate(CustomerCarBase):
    pass


class CustomerCarResponse(CustomerCarBase):
    id: int
    customer: PartialUserResponse | None = None
    car: CarResponse | None = None


class CustomerCarUpdate(CustomerCarBase):
    year: int | None = None
    license_plate: str | None = None
    car_id: int | None = None
    customer_id: int | None = None
