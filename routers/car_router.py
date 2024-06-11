from fastapi import APIRouter, Depends

from models.car_model import CarCreate, CarResponse, CarUpdate, CarQuery, Car
from routers.auth_router import CurrentAdminUser
from services.car_service import CarService

router = APIRouter()


@router.post("/create", response_model=CarResponse)
def create_car(
        _: CurrentAdminUser,
        car: CarCreate,
        car_service: CarService = Depends()
):
    return car_service.create(Car, car)


@router.get("/", response_model=list[CarResponse])
def read_cars(
        _: CurrentAdminUser,
        query: CarQuery = Depends(),
        car_service: CarService = Depends()
):
    return car_service.read(query)


@router.patch("/update/{car_id}", response_model=CarResponse)
def update_car(
        _: CurrentAdminUser,
        car_id: int,
        car: CarUpdate,
        car_service: CarService = Depends()
):
    return car_service.update(Car, car_id, car)


@router.delete("/delete/{car_id}")
def delete_car(
        _: CurrentAdminUser,
        car_id: int,
        car_service: CarService = Depends()
):
    return car_service.delete(Car, car_id)
