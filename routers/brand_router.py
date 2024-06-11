from fastapi import APIRouter, Depends

from models.brand_model import BrandCreate, BrandResponse, BrandUpdate, BrandQuery
from routers.auth_router import CurrentAdminUser
from services.brand_service import BrandService

router = APIRouter()


@router.post("/create", response_model=BrandResponse)
def create_brand(
        _: CurrentAdminUser,
        brand: BrandCreate,
        brand_service: BrandService = Depends()
):
    return brand_service.create(brand)


@router.get("/", response_model=list[BrandResponse])
def read_brands(
        _: CurrentAdminUser,
        query: BrandQuery = Depends(),
        brand_service: BrandService = Depends()
):
    return brand_service.read(query)


@router.patch("/update/{brand_id}", response_model=BrandResponse)
def update_brand(
        _: CurrentAdminUser,
        brand_id: int,
        brand: BrandUpdate,
        brand_service: BrandService = Depends()
):
    return brand_service.update(brand_id, brand)


@router.delete("/delete/{brand_id}")
def delete_brand(
        _: CurrentAdminUser,
        brand_id: int,
        brand_service: BrandService = Depends()
):
    return brand_service.delete(brand_id)
