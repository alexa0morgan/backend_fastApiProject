from sqlmodel import Field, SQLModel, Relationship

from models.brand import Brand, BrandResponse


class CarBase(SQLModel):
    model: str

    brand_id: int | None = Field(default=None, foreign_key="brand.id")


class Car(CarBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    deleted_at: str | None = None

    brand: Brand | None = Relationship(back_populates="cars")


class CarCreate(CarBase):
    pass


class CarResponse(CarBase):
    id: int
    brand: BrandResponse | None = None


class CarUpdate(CarBase):
    model: str | None = None
    brand_id: int | None = None
