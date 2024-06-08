from sqlmodel import SQLModel
from db import engine
from models import user, brand, car, customer_car, service

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
