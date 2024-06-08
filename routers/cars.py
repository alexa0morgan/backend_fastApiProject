from datetime import datetime, UTC

from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select

from db import CurrentSession
from models.car import Car, CarCreate, CarResponse, CarUpdate
from routers.auth import CurrentAdminUser

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
        car_id: int = Query(None),
        offset: int = Query(0),
        limit: int = Query(default=5, le=100)
):
    return session.exec(
        select(Car)
        .where(Car.deleted_at == None)
        .where(Car.id == car_id if car_id else True)
        .order_by(Car.id)
        .offset(offset)
        .limit(limit)
    ).all()


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
