from sqlmodel import SQLModel

from db import engine
from models import user_model, brand_model, car_model, customer_car_model, service_model, order_model, service_order_model

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
