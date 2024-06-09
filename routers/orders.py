from datetime import datetime, UTC, timedelta

from fastapi import APIRouter
from sqlmodel import select

from db import CurrentSession
from models.customer_car import CustomerCar
from models.order import Order, OrderCreate, OrderResponse
from models.service import Service
from models.user import Role
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
