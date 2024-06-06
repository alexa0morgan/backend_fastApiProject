from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select

from db import CurrentSession
from models.brand import Brand, BrandCreate, BrandResponse, BrandUpdate
from routers.auth import CurrentAdminUser

router = APIRouter()


@router.post("/create", response_model=BrandResponse)
def create_brand(
        session: CurrentSession,
        _: CurrentAdminUser,
        brand: BrandCreate,
):
    db_brand = Brand.model_validate(brand)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


@router.get("/", response_model=list[BrandResponse])
def read_brands(
        session: CurrentSession,
        _: CurrentAdminUser,
        brand_id: int = Query(None),
        brand_ids: list[int] = Query(None),
        name: str = Query(None),
        names: list[str] = Query(None),
        offset: int = Query(0),
        limit: int = Query(default=5, le=100)
):
    return session.exec(
        select(Brand)
        .where(Brand.deleted_at == None)  # выборка только неудаленных записей
        .where(Brand.id == brand_id if brand_id else True)
        .where(Brand.id.in_(brand_ids) if brand_ids else True)
        .where(Brand.name.like(f'%{name}%') if name else True)
        .where(Brand.name.in_(names) if names else True)
        .offset(offset)
        .limit(limit)
        .order_by(Brand.id)  # обратная сортировка Brand.id.desc()
    ).all()


@router.patch("/update/{brand_id}", response_model=BrandResponse)
def update_brand(
        session: CurrentSession,
        _: CurrentAdminUser,
        brand_id: int,
        brand: BrandUpdate,
):
    db_brand = session.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    brand_data = brand.model_dump(exclude_unset=True)  # exclude_unset=True - исключает неустановленные значения
    db_brand.sqlmodel_update(brand_data)  # обновление значений
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


@router.delete("/delete/{brand_id}", response_model=BrandResponse)
def delete_brand(
        session: CurrentSession,
        _: CurrentAdminUser,
        brand_id: int,
):
    db_brand = session.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    db_brand.deleted_at = str(datetime.now(timezone.utc)) + 'Z'
    session.commit()
    return {"message": "Brand deleted successfully"}