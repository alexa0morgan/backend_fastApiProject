from datetime import datetime, UTC

from models.brand_model import Brand, BrandCreate, BrandQuery, BrandUpdate
from services.base_service import BaseService


class BrandService(BaseService):

    def create(self, brand: BrandCreate) -> Brand:
        db_brand = Brand.model_validate(brand)
        return self.save_and_refresh(db_brand)

    def read(self, query: BrandQuery):
        options = [Brand.deleted_at == None]

        if query.id:
            options.append(Brand.id == query.id)
        if query.id_in:
            options.append(Brand.id.in_(query.id_in))
        if query.name:
            options.append(Brand.name.ilike(f'%{query.name}%'))
        if query.name_in:
            options.append(Brand.name.in_(query.name_in))

        return self.get_all(Brand, options, query)

    def update(self, brand_id: int, brand: BrandUpdate) -> Brand:
        db_brand = self.get_one(Brand, brand_id)
        brand_data = brand.model_dump(exclude_unset=True)  # exclude_unset=True - исключает неустановленные значения
        db_brand.sqlmodel_update(brand_data)
        return self.save_and_refresh(db_brand)

    def delete(self, brand_id: int):
        db_brand = self.get_one(Brand, brand_id)

        db_brand.deleted_at = datetime.now(UTC).isoformat()
        self.session.commit()
        return {"message": "Brand deleted successfully"}
