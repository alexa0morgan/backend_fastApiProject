from models.brand_model import Brand
from models.car_model import Car, CarCreate, CarQuery, CarUpdate
from services.base_service import BaseService


class CarService(BaseService):

    def create(self, car: CarCreate) -> Car:
        db_car = Car.model_validate(car)
        return self.save_and_refresh(db_car)

    def read(self, query: CarQuery):

        joins = set()

        options = [Car.deleted_at == None]

        if query.id:
            options.append(Car.id == query.id)
        if query.id_in:
            options.append(Car.id.in_(query.id_in))
        if query.model:
            options.append(Car.model.ilike(f'%{query.model}%'))
        if query.model_in:
            options.append(Car.model.in_(query.model_in))
        if query.brand_id:
            options.append(Car.brand_id == query.brand_id)
        if query.brand_id_in:
            options.append(Car.brand_id.in_(query.brand_id_in))
        if query.brand_name:
            joins.add(Car.brand)
            options.append(Brand.name.ilike(f'%{query.brand_name}%'))
        if query.brand_name_in:
            joins.add(Car.brand)
            options.append(Brand.name.in_(query.brand_name_in))

        return self.get_all(Car, options, query, list(joins))

    def update(self, car_id: int, car: CarUpdate):
        db_car = self.get_one(Car, car_id)
        car_data = car.model_dump(exclude_unset=True)  # exclude_unset=True - исключает неустановленные значения
        db_car.sqlmodel_update(car_data)
        return self.save_and_refresh(db_car)

    def delete(self, car_id: int):
        db_car = self.get_one(Car, car_id)

        self.mark_deleted(db_car)
        return {"message": "Car deleted successfully"}
