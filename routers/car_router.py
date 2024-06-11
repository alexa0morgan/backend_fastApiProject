from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException, Depends

from db import CurrentSession
from models.brand_model import Brand
from models.car_model import Car, CarCreate, CarResponse, CarUpdate, CarQuery
from routers.auth_router import CurrentAdminUser
from services.base_service import get_all

router = APIRouter()


@router.post("/create", response_model=CarResponse)
def create_car(
        session: CurrentSession,
        _: CurrentAdminUser,
        car: CarCreate,
):
    db_car = Car.model_validate(car)
    session.add(db_car)
    session.commit()
    session.refresh(db_car)
    return db_car


@router.get("/", response_model=list[CarResponse])
def read_cars(
        session: CurrentSession,
        _: CurrentAdminUser,
        query: CarQuery = Depends()
):
    joins = set()
    options = [Car.deleted_at == None]

    if query.id:
        options.append(Car.id == query.id)
    if query.id_in:
        options.append(Car.id.in_(query.id_in))
    if query.model:
        options.append(Car.model.ilike(f'%{query.model}%'))
    if query.model_in:
        options.append(Car.model.in_(query.model_in))
    if query.brand_id:
        options.append(Car.brand_id == query.brand_id)
    if query.brand_id_in:
        options.append(Car.brand_id.in_(query.brand_id_in))
    if query.brand_name:
        joins.add(Car.brand)
        options.append(Brand.name.ilike(f'%{query.brand_name}%'))
    if query.brand_name_in:
        joins.add(Car.brand)
        options.append(Brand.name.in_(query.brand_name_in))

    return get_all(session, Car, options, query, list(joins))


@router.patch("/update/{car_id}", response_model=CarResponse)
def update_car(
        session: CurrentSession,
        _: CurrentAdminUser,
        car_id: int,
        car: CarUpdate,
):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")

    car_data = car.model_dump(exclude_unset=True)  # exclude_unset=True - исключает неустановленные значения
    db_car.sqlmodel_update(car_data)  # обновление значений
    session.add(db_car)
    session.commit()
    session.refresh(db_car)
    return db_car


@router.delete("/delete/{car_id}")
def delete_car(
        session: CurrentSession,
        _: CurrentAdminUser,
        car_id: int,
):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")

    db_car.deleted_at = datetime.now(UTC).isoformat()
    session.commit()
    return {"message": "Car deleted successfully"}
