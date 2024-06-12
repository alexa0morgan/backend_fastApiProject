from models.brand_model import BrandCreate, BrandResponse, BrandUpdate, BrandQuery
from routers.crud_router import create_crud_router
from services.brand_service import BrandService

router = create_crud_router(
    create_model=BrandCreate,
    response_model=BrandResponse,
    update_model=BrandUpdate,
    query_model=BrandQuery,
    service_type=BrandService
)

