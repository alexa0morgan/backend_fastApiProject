from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException, Depends

import services.brand_service as BrandService
from db import CurrentSession
from models.brand_model import Brand, BrandCreate, BrandResponse, BrandUpdate, BrandQuery
from routers.auth_router import CurrentAdminUser
from services.base_service import get_all

router = APIRouter()


@router.post("/create", response_model=BrandResponse)
def create_brand(
        session: CurrentSession,
        _: CurrentAdminUser,
        brand: BrandCreate,
):
    return BrandService.create_brand(session, brand)


@router.get("/", response_model=list[BrandResponse])
def read_brands(
        session: CurrentSession,
        _: CurrentAdminUser,
        query: BrandQuery = Depends()

):
    options = [Brand.deleted_at == None]

    if query.id:
        options.append(Brand.id == query.id)
    if query.id_in:
        options.append(Brand.id.in_(query.id_in))
    if query.name:
        options.append(Brand.name.ilike(f'%{query.name}%'))
    if query.name_in:
        options.append(Brand.name.in_(query.name_in))

    return get_all(session, Brand, options, query)


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


@router.delete("/delete/{brand_id}")
def delete_brand(
        session: CurrentSession,
        _: CurrentAdminUser,
        brand_id: int,
):
    db_brand = session.get(Brand, brand_id)
    if not db_brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    db_brand.deleted_at = datetime.now(UTC).isoformat()
    session.commit()
    return {"message": "Brand deleted successfully"}
