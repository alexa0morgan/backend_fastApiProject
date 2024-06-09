from datetime import datetime, UTC, timedelta

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db import CurrentSession
from models.customer_car import CustomerCar
from models.order import Order, OrderCreate, OrderResponse, OrderUpdate, Status, OrderAddServices
from models.service import Service
from models.user import Role, User
from routers.auth import CurrentAdminUser, CurrentUser

router = APIRouter()


@router.post("/create", response_model=OrderResponse)
def create_order(
        session: CurrentSession,
        _: CurrentAdminUser,
        order: OrderCreate
):
    services = session.exec(select(Service).where(Service.id.in_(order.services))).all()
    total_time = timedelta(seconds=sum([service.minTime for service in services]))
    db_order = Order.model_validate(
        order,
        update={
            "start_date": datetime.now(UTC).isoformat(),
            "end_date": (datetime.now(UTC) + total_time).isoformat(),
            "services": services
        }
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.get("/", response_model=list[OrderResponse])
def read_orders(
        session: CurrentSession,
        current_user: CurrentUser,
        order_id: int = None,
        offset: int = 0,
        limit: int = 5

):
    if current_user.role_id == Role.admin:
        return session.exec(
            select(Order)
            .where(Order.deleted_at == None)
            .where(Order.id == order_id if order_id else True)
            .order_by(Order.id)
            .offset(offset)
            .limit(limit)
        ).all()
    if current_user.role_id == Role.employee:
        return session.exec(
            select(Order)
            .where(Order.deleted_at == None)
            .where(Order.employee_id == current_user.id)
            .where(Order.id == order_id if order_id else True)
            .order_by(Order.id)
            .offset(offset)
            .limit(limit)
        ).all()
    if current_user.role_id == Role.client:
        return session.exec(
            select(Order)
            .join(Order.customer_car)
            .where(Order.deleted_at == None)
            .where(CustomerCar.customer_id == current_user.id)
            .where(Order.id == order_id if order_id else True)
            .order_by(Order.id)
            .offset(offset)
            .limit(limit)
        ).all()


@router.patch("/update/{order_id}", response_model=OrderResponse)
def update_order(
        session: CurrentSession,
        _: CurrentAdminUser,
        order_id: int,
        order: OrderUpdate
):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_data = order.model_dump(exclude_unset=True)
    db_order.sqlmodel_update(order_data)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.delete("/delete/{order_id}")
def delete_order(
        session: CurrentSession,
        _: CurrentAdminUser,
        order_id: int
):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order.deleted_at = datetime.now(UTC).isoformat()
    session.commit()
    return {"message": "Order deleted successfully"}


@router.post("/toggle_status/{order_id}", response_model=OrderResponse)
def complete_order(
        session: CurrentSession,
        _: CurrentAdminUser,
        order_id: int
):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db_order.status == Status.completed:
        db_order.status = Status.in_progress
    else:
        db_order.status = Status.completed
        db_customer = session.get(User, db_order.customer_car.customer_id)
        if db_customer.send_notifications:
            print(f"\n\n\n\nSending notification to {db_customer.email}\n\n\n\n")

    session.commit()
    session.refresh(db_order)
    return db_order


@router.post("/add_service/{order_id}", response_model=OrderResponse)
def add_service_to_order(
        session: CurrentSession,
        _: CurrentAdminUser,
        order_id: int,
        new_services: OrderAddServices  # id новых услуг

):
    db_order = session.get(Order, order_id)  # данные заказа
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    for service in db_order.services:  # данные текущих услуг
        if service.id in new_services.service_ids:
            raise HTTPException(status_code=422, detail=f"Service {service.name} already added to order")

    services = session.exec(
        select(Service)
        .where(Service.id.in_(new_services.service_ids))
    ).all()  # данные новых услуг

    for id in new_services.service_ids:
        if id not in [service.id for service in services]:
            raise HTTPException(status_code=404, detail=f"Service with id={id} not found")

    db_order.services.extend(services)
    total_time = timedelta(seconds=sum([service.minTime for service in db_order.services]))
    db_order.end_date = (datetime.fromisoformat(db_order.start_date) + total_time).isoformat()

    session.commit()
    session.refresh(db_order)
    return db_order
