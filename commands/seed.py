from sqlmodel import Session

from db import engine
from models.brand_model import Brand
from models.car_model import Car
from models.customer_car_model import CustomerCar
from models.order_model import Order
from models.service_model import Service
from models.user_model import User, Role
from models.service_order_model import ServiceOrder  # noqa
from services.auth_service import AuthService

with Session(engine) as session:
    session.add(User(
        first_name="John",
        last_name="Doe",
        patronymic="Smith",
        email="jdoe@example.com",
        role_id=Role.admin,
        send_notifications=True,
        hashed_password=AuthService.hash_password("password"),
    ))
    session.add(User(
        first_name="Jane",
        last_name="Doe",
        email="jadoe@example.com",
        role_id=Role.admin,
        send_notifications=True,
        hashed_password=AuthService.hash_password("password"),
    ))

    session.add(User(
        first_name="Alice",
        last_name="McDonald",
        email="amcdonald@example.com",
        role_id=Role.employee,
        send_notifications=True,
        hashed_password=AuthService.hash_password("password"),
    ))
    session.add(User(
        first_name="Alex",
        last_name="Johnson",
        email="ajonson@example.com",
        role_id=Role.employee,
        send_notifications=True,
        hashed_password=AuthService.hash_password("password"),
    ))

    session.add(User(
        first_name="Bob",
        last_name="Brown",
        email="bbrown@example.net",
        role_id=Role.client,
        send_notifications=False,
        hashed_password=AuthService.hash_password("password"),
    ))
    session.add(User(
        email="cust@example.com",
        first_name="Customer2",
        last_name="User",
        role_id=Role.client,
        hashed_password=AuthService.hash_password("password"),
        send_notifications=True
    ))

    session.add(Brand(name="Pagani"))
    session.add(Brand(name="Ferrari"))
    session.add(Brand(name="Lamborghini"))
    session.add(Brand(name="McLaren"))
    session.add(Brand(name="Bugatti"))
    session.add(Brand(name="Aston Martin"))
    session.add(Brand(name="Porsche"))
    session.add(Brand(name="Koenigsegg"))

    # Pagani models
    session.add(Car(model="Huayra", brand_id=1))
    session.add(Car(model="Zonda", brand_id=1))

    # Ferrari models
    session.add(Car(model="488 GTB", brand_id=2))
    session.add(Car(model="LaFerrari", brand_id=2))

    # Lamborghini models
    session.add(Car(model="Aventador", brand_id=3))
    session.add(Car(model="Huracan", brand_id=3))

    # McLaren models
    session.add(Car(model="720S", brand_id=4))
    session.add(Car(model="P1", brand_id=4))

    # Bugatti models
    session.add(Car(model="Chiron", brand_id=5))
    session.add(Car(model="Veyron", brand_id=5))

    # Aston Martin models
    session.add(Car(model="DB11", brand_id=6))
    session.add(Car(model="Vantage", brand_id=6))

    # Porsche models
    session.add(Car(model="911", brand_id=7))
    session.add(Car(model="Cayman", brand_id=7))

    # Koenigsegg models
    session.add(Car(model="Agera", brand_id=8))
    session.add(Car(model="Regera", brand_id=8))

    session.add(CustomerCar(
        car_id=1,
        customer_id=3,
        year=2010,
        license_plate="A123AA"
    ))
    session.add(CustomerCar(
        car_id=3,
        customer_id=4,
        year=2020,
        license_plate="B456BB"
    ))

    service1 = Service(
        name="Oil change",
        minPrice=2000_00,
        minTime=1800,
    )
    session.add(service1)

    service2 = Service(
        name="Tire replacement",
        minPrice=5000_00,
        minTime=3600,
    )
    session.add(service2)

    service3 = Service(
        name="Wheel alignment",
        minPrice=3000_00,
        minTime=2400,
    )
    session.add(service3)

    service4 = Service(
        name="Brake pad replacement",
        minPrice=7000_00,
        minTime=3600,
    )
    session.add(service4)

    service5 = Service(
        name="Battery replacement",
        minPrice=4000_00,
        minTime=1800,
    )
    session.add(service5)

    session.add(Order(
        administrator_id=1,
        employee_id=2,
        customer_car_id=1,
        services=[service1, service2, service3],
        start_date="2021-10-01T12:00:00Z",
        end_date="2021-10-01T15:00:00Z",
    ))
    session.add(Order(
        administrator_id=1,
        employee_id=2,
        customer_car_id=2,
        services=[service4, service5],
        start_date="2021-10-01T12:00:00Z",
        end_date="2021-10-01T13:30:00Z",
    ))
    session.add(Order(
        administrator_id=1,
        employee_id=2,
        customer_car_id=1,
        services=[service1, service2, service3],
        start_date="2021-10-01T12:00:00Z",
        end_date="2021-10-01T14:10:00Z",
    ))
    session.add(Order(
        administrator_id=1,
        employee_id=2,
        customer_car_id=2,
        services=[service4, service5],
        start_date="2021-10-01T12:00:00Z",
        end_date="2021-10-01T13:30:00Z",
    ))

    session.commit()
