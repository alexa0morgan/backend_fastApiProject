from fastapi import Depends

from models.order_model import OrderCreate, OrderResponse, OrderUpdate, OrderAddServices, OrderQuery
from routers.crud_router import create_crud_router
from services.auth_service import AuthService
from services.order_service import OrderService

router = create_crud_router(
    create_model=OrderCreate,
    response_model=OrderResponse,
    update_model=OrderUpdate,
    query_model=OrderQuery,
    service_type=OrderService,
    ignore_read=True,
)


@router.get("/", response_model=list[OrderResponse])
def read(
        _: AuthService.CurrentAdminUser,
        user: AuthService.CurrentUser,
        query: OrderQuery = Depends(),
        service: OrderService = Depends(),
):
    return service.read(query, user)


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
