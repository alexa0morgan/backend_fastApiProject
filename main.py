import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel

if os.getenv("ENV") != "test":
    load_dotenv()

from db import engine
from routers.auth_router import router as auth_router
from routers.brand_router import router as brands_router
from routers.car_router import router as cars_router
from routers.customer_car_router import router as customer_cars_router
from routers.order_router import router as orders_router
from routers.service_router import router as services_router
from routers.user_router import router as users_router

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(brands_router, prefix="/brands", tags=["brands"])
app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(customer_cars_router, prefix="/customer_cars", tags=["customer_cars"])
app.include_router(services_router, prefix="/services", tags=["services"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
