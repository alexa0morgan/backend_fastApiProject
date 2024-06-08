from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db import CurrentSession
from models.customer_car import CustomerCarCreate, CustomerCar, CustomerCarResponse, CustomerCarUpdate
from routers.auth import CurrentAdminUser

router = APIRouter()


@router.post("/create", response_model=CustomerCarResponse)
def create_customer_car(
        session: CurrentSession,
        _: CurrentAdminUser,
        customer_car: CustomerCarCreate,
):
    db_customer_car = CustomerCar.model_validate(customer_car)
    session.add(db_customer_car)
    session.commit()
    session.refresh(db_customer_car)
    return db_customer_car


@router.get("/", response_model=list[CustomerCarResponse])
def read_customer_cars(
        session: CurrentSession,
        _: CurrentAdminUser,
        customer_car_id: int = None,
        offset: int = 0,
        limit: int = 5
):
    return session.exec(
        select(CustomerCar)
        .where(CustomerCar.deleted_at == None)
        .where(CustomerCar.id == customer_car_id if customer_car_id else True)
        .order_by(CustomerCar.id)
        .offset(offset)
        .limit(limit)
    ).all()


@router.patch("/update/{customer_car_id}", response_model=CustomerCarResponse)
def update_customer_car(
        session: CurrentSession,
        _: CurrentAdminUser,
        customer_car_id: int,
        customer_car: CustomerCarUpdate,
):
    db_customer_car = session.get(CustomerCar, customer_car_id)
    if not db_customer_car:
        raise HTTPException(status_code=404, detail="Customer car not found")

    customer_car_data = customer_car.model_dump(exclude_unset=True)
    db_customer_car.sqlmodel_update(customer_car_data)
    session.add(db_customer_car)
    session.commit()
    session.refresh(db_customer_car)
    return db_customer_car


@router.delete("/delete/{customer_car_id}")
def delete_customer_car(
        session: CurrentSession,
        _: CurrentAdminUser,
        customer_car_id: int,
):
    db_customer_car = session.get(CustomerCar, customer_car_id)
    if not db_customer_car:
        raise HTTPException(status_code=404, detail="Customer car not found")

    db_customer_car.deleted_at = str(datetime.now(timezone.utc)) + 'Z'
    session.commit()
    return {'message': "Customer car deleted successfully"}
