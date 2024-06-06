from fastapi import FastAPI
from sqlmodel import SQLModel

from db import engine
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.brands import router as brands_router
from routers.cars import router as cars_router

app = FastAPI()

app.include_router(auth_router, tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(brands_router, prefix="/brands", tags=["brands"])
app.include_router(cars_router, prefix="/cars", tags=["cars"])


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
