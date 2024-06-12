from models.service_model import ServiceResponse, ServiceCreate, ServiceUpdate, ServiceQuery
from routers.crud_router import create_crud_router
from services.service_service import ServiceService

router = create_crud_router(
    create_model=ServiceCreate,
    response_model=ServiceResponse,
    update_model=ServiceUpdate,
    query_model=ServiceQuery,
    service_type=ServiceService
)
