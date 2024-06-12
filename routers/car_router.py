from models.car_model import CarCreate, CarResponse, CarUpdate, CarQuery
from routers.crud_router import create_crud_router
from services.car_service import CarService

router = create_crud_router(
    create_model=CarCreate,
    response_model=CarResponse,
    update_model=CarUpdate,
    query_model=CarQuery,
    service_type=CarService
)
