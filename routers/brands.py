from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select

from db import engine
from models.brand import Brand, BrandCreate, BrandResponse, BrandUpdate
from routers.auth import CurrentAdminUser

router = APIRouter()


@router.post("/create", response_model=BrandResponse)
def create_brand(brand: BrandCreate, _: CurrentAdminUser):
    with Session(engine) as session:
        db_brand = Brand.model_validate(brand)
        session.add(db_brand)
        session.commit()
        session.refresh(db_brand)
        return db_brand


@router.get("/", response_model=list[BrandResponse])
def read_brands(_: CurrentAdminUser,
                brand_id: int = Query(None),
                brand_ids: list[int] = Query(None),
                name: str = Query(None),
                names: list[str] = Query(None),
                offset: int = 0,
                limit: int = Query(default=5, le=100)
                ):
    with (Session(engine) as session):
        return session.exec(select(Brand)
                            .where(Brand.id == brand_id if brand_id else True)
                            .where(Brand.id.in_(brand_ids) if brand_ids else True)
                            .where(Brand.name.like(f'%{name}%') if name else True)
                            .where(Brand.name.in_(names) if names else True)
                            .offset(offset)
                            .limit(limit)
                            .order_by(Brand.id)  # обратная сортировка Brand.id.desc()
                            ).all()


@router.patch("/update/{brand_id}", response_model=BrandResponse)
def update_brand(brand_id: int, brand: BrandUpdate, _: CurrentAdminUser):
    with Session(engine) as session:
        db_brand = session.get(Brand, brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
        brand_data = brand.model_dump(exclude_unset=True)  # exclude_unset=True - исключает неустановленные значения
        db_brand.sqlmodel_update(brand_data)  # обновление значений
        session.add(db_brand)
        session.commit()
        session.refresh(db_brand)
        return db_brand
