from sqlmodel import Field, SQLModel


class BrandBase(SQLModel):
    name: str
    deleted_at: str | None = None


class Brand(BrandBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BrandCreate(BrandBase):
    pass


class BrandResponse(BrandBase):
    id: int


class BrandUpdate(BrandBase):
    name: str | None = None
