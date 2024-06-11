from fastapi import APIRouter, Depends

from db import CurrentSession
from models.customer_car_model import CustomerCarCreate, CustomerCar, CustomerCarResponse, CustomerCarUpdate, \
    CustomerCarQuery
from routers.auth_router import CurrentAdminUser
from services.customer_car_service import CustomerCarService

router = APIRouter()


@router.post("/create", response_model=CustomerCarResponse)
def create_customer_car(
        _: CurrentAdminUser,
        customer_car: CustomerCarCreate,
        customer_car_service: CustomerCarService = Depends()
):
    return customer_car_service.create(CustomerCar, customer_car)


@router.get("/", response_model=list[CustomerCarResponse])
def read_customer_cars(
        session: CurrentSession,
        _: CurrentAdminUser,
        query: CustomerCarQuery = Depends(),
        customer_car_service: CustomerCarService = Depends()
):
    return customer_car_service.read(query)


@router.patch("/update/{customer_car_id}", response_model=CustomerCarResponse)
def update_customer_car(
        _: CurrentAdminUser,
        customer_car_id: int,
        customer_car: CustomerCarUpdate,
        customer_car_service: CustomerCarService = Depends()

):
    return customer_car_service.update(CustomerCar, customer_car_id, customer_car)


@router.delete("/delete/{customer_car_id}")
def delete_customer_car(
        _: CurrentAdminUser,
        customer_car_id: int,
        customer_car_service: CustomerCarService = Depends()

):
    return customer_car_service.delete(CustomerCar, customer_car_id)
