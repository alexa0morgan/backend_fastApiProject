from fastapi import APIRouter, Depends

from models.service_model import ServiceResponse, ServiceCreate, ServiceUpdate, ServiceQuery
from services.auth_service import AuthService
from services.service_service import ServiceService

router = APIRouter()


@router.post("/create", response_model=ServiceResponse)
def create_service(
        _: AuthService.CurrentAdminUser,
        service: ServiceCreate,
        service_service: ServiceService = Depends()
):
    return service_service.create(service)


@router.get("/", response_model=list[ServiceResponse])
def read_services(
        _: AuthService.CurrentAdminUser,
        query: ServiceQuery = Depends(),
        service_service: ServiceService = Depends()
):
    service_service.read(query)


@router.patch("/update/{service_id}", response_model=ServiceResponse)
def update_service(
        _: AuthService.CurrentAdminUser,
        service_id: int,
        service: ServiceUpdate,
        service_service: ServiceService = Depends()

):
    return service_service.update(service_id, service)


@router.delete("/delete/{service_id}")
def delete_service(
        _: AuthService.CurrentAdminUser,
        service_id: int,
        service_service: ServiceService = Depends()

):
    return service_service.delete(service_id)
