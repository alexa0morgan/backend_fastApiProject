from models.car_model import Car
from models.customer_car_model import CustomerCar, CustomerCarQuery
from models.user_model import User
from services.base_service import BaseService


class CustomerCarService(BaseService):
    cls = CustomerCar

    def read(self, query: CustomerCarQuery):
        joins = set()

        options = [CustomerCar.deleted_at == None]

        if query.id:
            options.append(CustomerCar.id == query.id)
        if query.id_in:
            options.append(CustomerCar.id.in_(query.id_in))
        if query.car_id:
            options.append(CustomerCar.car_id == query.car_id)
        if query.car_id_in:
            options.append(CustomerCar.car_id.in_(query.car_id_in))
        if query.customer_id:
            options.append(CustomerCar.customer_id == query.customer_id)
        if query.customer_id_in:
            options.append(CustomerCar.customer_id.in_(query.customer_id_in))
        if query.year:
            options.append(CustomerCar.year == query.year)
        if query.year_gt:
            options.append(CustomerCar.year > query.year_gt)
        if query.year_lt:
            options.append(CustomerCar.year < query.year_lt)
        if query.license_plate:
            options.append(CustomerCar.license_plate.ilike(f'%{query.license_plate}%'))
        if query.customer_first_name:
            joins.add(CustomerCar.customer)
            options.append(User.first_name.ilike(f'%{query.customer_first_name}%'))
        if query.customer_first_name_in:
            joins.add(CustomerCar.customer)
            options.append(User.first_name.in_(query.customer_first_name_in))
        if query.customer_last_name:
            joins.add(CustomerCar.customer)
            options.append(User.last_name.ilike(f'%{query.customer_last_name}%'))
        if query.customer_last_name_in:
            joins.add(CustomerCar.customer)
            options.append(User.last_name.in_(query.customer_last_name_in))
        if query.car_model:
            joins.add(CustomerCar.car)
            options.append(Car.model.ilike(f'%{query.car_model}%'))
        if query.car_model_in:
            joins.add(CustomerCar.car)
            options.append(Car.model.in_(query.car_model_in))

        return self.get_all(CustomerCar, options, query, list(joins))
