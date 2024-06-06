from sqlmodel import Field, SQLModel, Relationship


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
