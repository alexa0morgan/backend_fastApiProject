from models.service_model import ServiceQuery, Service
from services.base_service import BaseService


class ServiceService(BaseService):
    cls = Service

    def read(self, query: ServiceQuery):
        options = [Service.deleted_at == None]

        if query.id:
            options.append(Service.id == query.id)
        if query.id_in:
            options.append(Service.id.in_(query.id_in))
        if query.name:
            options.append(Service.name.ilike(f'%{query.name}%'))
        if query.price:
            options.append(Service.minPrice == query.price)
        if query.price_gt:
            options.append(Service.minPrice > query.price_gt)
        if query.price_lt:
            options.append(Service.minPrice < query.price_lt)
        if query.price_in:
            options.append(Service.minPrice.in_(query.price_in))
        if query.time:
            options.append(Service.minTime == query.time)
        if query.time_gt:
            options.append(Service.minTime > query.time_gt)
        if query.time_lt:
            options.append(Service.minTime < query.time_lt)
        if query.time_in:
            options.append(Service.minTime.in_(query.time_in))

        return self.get_all(Service, options, query)
