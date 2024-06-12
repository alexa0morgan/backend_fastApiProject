from models.customer_car_model import CustomerCarCreate, CustomerCarResponse, CustomerCarUpdate, \
    CustomerCarQuery
from routers.crud_router import create_crud_router
from services.customer_car_service import CustomerCarService

router = create_crud_router(
    create_model=CustomerCarCreate,
    response_model=CustomerCarResponse,
    update_model=CustomerCarUpdate,
    query_model=CustomerCarQuery,
    service_type=CustomerCarService
)
