from datetime import datetime, UTC

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db import CurrentSession
from models.service import ServiceResponse, ServiceCreate, Service, ServiceUpdate
from routers.auth import CurrentAdminUser

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
        service_id: int = None,
        offset: int = 0,
        limit: int = 5
):
    return session.exec(
        select(Service)
        .where(Service.deleted_at == None)
        .where(Service.id == service_id if service_id else True)
        .order_by(Service.id)
        .offset(offset)
        .limit(limit)
    ).all()


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
