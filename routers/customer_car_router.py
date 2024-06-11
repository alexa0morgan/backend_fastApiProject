from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException, Depends

from db import CurrentSession
from models.car_model import Car
from models.customer_car_model import CustomerCarCreate, CustomerCar, CustomerCarResponse, CustomerCarUpdate, \
    CustomerCarQuery
from models.user_model import User
from routers.auth_router import CurrentAdminUser
from services.base_service import get_all

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
        query: CustomerCarQuery = Depends()
):
    joins = set()

    options = [CustomerCar.deleted_at == None]

    if query.id:
        options.append(CustomerCar.id == query.id)
    if query.id_in:
        options.append(CustomerCar.id.in_(query.id_in))
    if query.car_id:
        options.append(CustomerCar.car_id == query.car_id)
    if query.car_id_in:
        options.append(CustomerCar.car_id.in_(query.car_id_in))
    if query.customer_id:
        options.append(CustomerCar.customer_id == query.customer_id)
    if query.customer_id_in:
        options.append(CustomerCar.customer_id.in_(query.customer_id_in))
    if query.year:
        options.append(CustomerCar.year == query.year)
    if query.year_gt:
        options.append(CustomerCar.year > query.year_gt)
    if query.year_lt:
        options.append(CustomerCar.year < query.year_lt)
    if query.license_plate:
        options.append(CustomerCar.license_plate.ilike(f'%{query.license_plate}%'))
    if query.customer_first_name:
        joins.add(CustomerCar.customer)
        options.append(User.first_name.ilike(f'%{query.customer_first_name}%'))
    if query.customer_first_name_in:
        joins.add(CustomerCar.customer)
        options.append(User.first_name.in_(query.customer_first_name_in))
    if query.customer_last_name:
        joins.add(CustomerCar.customer)
        options.append(User.last_name.ilike(f'%{query.customer_last_name}%'))
    if query.customer_last_name_in:
        joins.add(CustomerCar.customer)
        options.append(User.last_name.in_(query.customer_last_name_in))
    if query.car_model:
        joins.add(CustomerCar.car)
        options.append(Car.model.ilike(f'%{query.car_model}%'))
    if query.car_model_in:
        joins.add(CustomerCar.car)
        options.append(Car.model.in_(query.car_model_in))

    return get_all(session, CustomerCar, options, query, list(joins))


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

    db_customer_car.deleted_at = datetime.now(UTC).isoformat()
    session.commit()
    return {'message': "Customer car deleted successfully"}
