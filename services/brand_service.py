from fastapi import Query
from sqlmodel import Session

from models.brand_model import Brand, BrandCreate


def create_brand(session: Session, brand: BrandCreate) -> Brand:
    db_brand = Brand.model_validate(brand)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand
