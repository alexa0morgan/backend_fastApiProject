from models.brand_model import Brand, BrandQuery
from services.base_service import BaseService


class BrandService(BaseService):
    cls = Brand

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

        return self.get_all(options, query)
