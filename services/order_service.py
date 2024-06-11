from datetime import timedelta, datetime, UTC

from fastapi import HTTPException, status
from sqlmodel import select

from models.customer_car_model import CustomerCar
from models.order_model import Order, OrderQuery, OrderCreate, Status, OrderAddServices
from models.service_model import Service
from models.user_model import User, Role
from services.base_service import BaseService


class OrderService(BaseService):
    cls = Order

    def create(self, order: OrderCreate) -> Order:
        services = self.session.exec(select(Service).where(Service.id.in_(order.services))).all()
        total_time = timedelta(seconds=sum([service.minTime for service in services]))
        db_order = Order.model_validate(
            order,
            update={
                "start_date": datetime.now(UTC).isoformat(),
                "end_date": (datetime.now(UTC) + total_time).isoformat(),
                "services": services
            }
        )
        return self.save_and_refresh(db_order)

    def read(self, query: OrderQuery, current_user: User):
        joins = set()

        options = [Order.deleted_at == None]

        if query.id:
            options.append(Order.id == query.id)
        if query.id_in:
            options.append(Order.id.in_(query.id_in))
        if query.customer_car_id:
            options.append(Order.customer_car_id == query.customer_car_id)
        if query.customer_car_id_in:
            options.append(Order.customer_car_id.in_(query.customer_car_id_in))
        if query.customer_car_year:
            joins.add(Order.customer_car)
            options.append(CustomerCar.year == query.customer_car_year)
        if query.customer_car_year_gt:
            joins.add(Order.customer_car)
            options.append(CustomerCar.year > query.customer_car_year_gt)
        if query.customer_car_year_lt:
            joins.add(Order.customer_car)
            options.append(CustomerCar.year < query.customer_car_year_lt)
        if query.customer_car_license_plate:
            joins.add(Order.customer_car)
            options.append(CustomerCar.license_plate.ilike(f'%{query.customer_car_license_plate}%'))
        if query.customer_id:
            joins.add(Order.customer_car)
            options.append(CustomerCar.customer_id == query.customer_id)
        if query.customer_id_in:
            joins.add(Order.customer_car)
            options.append(CustomerCar.customer_id.in_(query.customer_id_in))
        if query.administrator_id:
            options.append(Order.administrator_id == query.administrator_id)
        if query.administrator_id_in:
            options.append(Order.administrator_id.in_(query.administrator_id_in))
        if query.employee_id:
            options.append(Order.employee_id == query.employee_id)
        if query.employee_id_in:
            options.append(Order.employee_id.in_(query.employee_id_in))
        if query.status:
            options.append(Order.status == query.status)
        if query.start_date_gte:
            options.append(Order.start_date >= query.start_date_gte)
        if query.start_date_lte:
            options.append(Order.start_date <= query.start_date_lte)
        if query.end_date_gte:
            options.append(Order.end_date >= query.end_date_gte)
        if query.end_date_lte:
            options.append(Order.end_date <= query.end_date_lte)

        if current_user.role_id == Role.employee:
            options.append(Order.employee_id == current_user.id)
        if current_user.role_id == Role.client:
            joins.add(Order.customer_car)
            options.append(CustomerCar.customer_id == current_user.id)

        return self.get_all(Order, options, query, list(joins))

    def toggle_status(self, order_id: int):
        db_order = self.get_one(Order, order_id)

        if db_order.status == Status.completed:
            db_order.status = Status.in_progress
        else:
            db_order.status = Status.completed
            db_customer = self.session.get(User, db_order.customer_car.customer_id)
            if db_customer.send_notifications:
                print(f"\n\n\n\nSending notification to {db_customer.email}\n\n\n\n")

        self.session.commit()
        self.session.refresh(db_order)
        return db_order

    def add_services(self, order_id: int, new_services: OrderAddServices):
        db_order = self.get_one(Order, order_id)

        for service in db_order.services:  # данные текущих услуг
            if service.id in new_services.service_ids:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    detail=f"Service {service.name} already added to order")

        services = self.session.exec(
            select(Service)
            .where(Service.id.in_(new_services.service_ids))
        ).all()  # данные новых услуг

        for id in new_services.service_ids:
            if id not in [service.id for service in services]:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service with id={id} not found")

        db_order.services.extend(services)
        total_time = timedelta(seconds=sum([service.minTime for service in db_order.services]))
        db_order.end_date = (datetime.fromisoformat(db_order.start_date) + total_time).isoformat()

        self.session.commit()
        self.session.refresh(db_order)
        return db_order
