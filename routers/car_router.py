from fastapi import APIRouter, Depends

from models.car_model import CarCreate, CarResponse, CarUpdate, CarQuery
from services.auth_service import AuthService
from services.car_service import CarService

router = APIRouter()


@router.post("/create", response_model=CarResponse)
def create_car(
        _: AuthService.CurrentAdminUser,
        car: CarCreate,
        car_service: CarService = Depends()
):
    return car_service.create(car)


@router.get("/", response_model=list[CarResponse])
def read_cars(
        _: AuthService.CurrentAdminUser,
        query: CarQuery = Depends(),
        car_service: CarService = Depends()
):
    return car_service.read(query)


@router.patch("/update/{car_id}", response_model=CarResponse)
def update_car(
        _: AuthService.CurrentAdminUser,
        car_id: int,
        car: CarUpdate,
        car_service: CarService = Depends()
):
    return car_service.update(car_id, car)


@router.delete("/delete/{car_id}")
def delete_car(
        _: AuthService.CurrentAdminUser,
        car_id: int,
        car_service: CarService = Depends()
):
    return car_service.delete(car_id)
