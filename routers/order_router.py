from fastapi import APIRouter, Depends

from models.order_model import OrderCreate, OrderResponse, OrderUpdate, OrderAddServices, OrderQuery
from services.auth_service import AuthService
from services.order_service import OrderService

router = APIRouter()


@router.post("/create", response_model=OrderResponse)
def create_order(
        _: AuthService.CurrentAdminUser,
        order: OrderCreate,
        order_service: OrderService = Depends()
):
    return order_service.create(order)


@router.get("/", response_model=list[OrderResponse])
def read_orders(
        current_user: AuthService.CurrentUser,
        query: OrderQuery = Depends(),
        order_service: OrderService = Depends()
):
    return order_service.read(query, current_user)


@router.patch("/update/{order_id}", response_model=OrderResponse)
def update_order(
        _: AuthService.CurrentAdminUser,
        order_id: int,
        order: OrderUpdate,
        order_service: OrderService = Depends()
):
    return order_service.update(order_id, order)


@router.delete("/delete/{order_id}")
def delete_order(
        _: AuthService.CurrentAdminUser,
        order_id: int,
        order_service: OrderService = Depends()
):
    return order_service.delete(order_id)


@router.post("/toggle_status/{order_id}", response_model=OrderResponse)
def complete_order(
        _: AuthService.CurrentAdminUser,
        order_id: int,
        order_service: OrderService = Depends()

):
    return order_service.toggle_status(order_id)


@router.post("/add_service/{order_id}", response_model=OrderResponse)
def add_services_to_order(
        _: AuthService.CurrentAdminUser,
        order_id: int,
        new_services: OrderAddServices,  # id новых услуг
        order_service: OrderService = Depends()

):
    return order_service.add_services(order_id, new_services)
