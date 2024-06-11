from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select

from db import CurrentSession
from models.service_model import ServiceResponse, ServiceCreate, Service, ServiceUpdate, ServiceQuery
from routers.auth_router import CurrentAdminUser
from services.base_service import get_all

router = APIRouter()


@router.post("/create", response_model=ServiceResponse)
def create_service(
        session: CurrentSession,
        _: CurrentAdminUser,
        service: ServiceCreate,
):
    db_service = Service.model_validate(service)
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service


@router.get("/", response_model=list[ServiceResponse])
def read_services(
        session: CurrentSession,
        _: CurrentAdminUser,
        query: ServiceQuery = Depends(),
):
    options = [Service.deleted_at == None]

    if query.id:
        options.append(Service.id == query.id)
    if query.id_in:
        options.append(Service.id.in_(query.id_in))
    if query.name:
        options.append(Service.name.ilike(f'%{query.name}%'))
    if query.price:
        options.append(Service.minPrice == query.price)
    if query.price_gt:
        options.append(Service.minPrice > query.price_gt)
    if query.price_lt:
        options.append(Service.minPrice < query.price_lt)
    if query.price_in:
        options.append(Service.minPrice.in_(query.price_in))
    if query.time:
        options.append(Service.minTime == query.time)
    if query.time_gt:
        options.append(Service.minTime > query.time_gt)
    if query.time_lt:
        options.append(Service.minTime < query.time_lt)
    if query.time_in:
        options.append(Service.minTime.in_(query.time_in))

    return get_all(session, Service, options, query)


@router.patch("/update/{service_id}", response_model=ServiceResponse)
def update_service(
        session: CurrentSession,
        _: CurrentAdminUser,
        service_id: int,
        service: ServiceUpdate,
):
    db_service = session.get(Service, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    service_data = service.model_dump(exclude_unset=True)
    db_service.sqlmodel_update(service_data)
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service


@router.delete("/delete/{service_id}")
def delete_service(
        session: CurrentSession,
        _: CurrentAdminUser,
        service_id: int,
):
    db_service = session.get(Service, service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    db_service.deleted_at = datetime.now(UTC).isoformat()
    session.commit()
    return {"message": "Service deleted successfully"}
