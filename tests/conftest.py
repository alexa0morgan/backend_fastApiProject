import os

import pytest
from fastapi.testclient import TestClient

os.environ["ENV"] = "test"
os.environ["SECRET_KEY"] = "secretkey"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ["DATABASE_URL"] = "sqlite:///test_database.db"

import commands.recreate  # noqa
import commands.seed  # noqa

from main import app  # noqa


@pytest.fixture(scope="session")
def guest_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session")
def customer_client(guest_client):
    client = TestClient(app)
    response = client.post(
        "/token",
        data={"username": "bbrown@example.net", "password": "password"},
    )
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client


@pytest.fixture(scope="session")
def employee_client(guest_client):
    client = TestClient(app)
    response = client.post(
        "/token",
        data={"username": "ajonson@example.com", "password": "password"},
    )
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client


@pytest.fixture(scope="session")
def admin_client(guest_client):
    client = TestClient(app)
    response = client.post(
        "/token",
        data={"username": "jdoe@example.com", "password": "password"},
    )
    token = response.json()["access_token"]
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client
