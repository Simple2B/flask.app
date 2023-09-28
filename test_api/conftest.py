from typing import Generator
import pytest
from dotenv import load_dotenv

load_dotenv("test_api/test.env")

# flake8: noqa F402
from fastapi.testclient import TestClient
from sqlalchemy import orm

from app import models as m
from app import schema as s

from api import app
from .test_data import TestData


@pytest.fixture
def db(test_data: TestData) -> Generator[orm.Session, None, None]:
    from app.database import db, get_db

    with db.Session() as session:
        db.Model.metadata.drop_all(bind=session.bind)
        db.Model.metadata.create_all(bind=session.bind)
        for test_user in test_data.test_users:
            session.add(
                m.User(
                    username=test_user.username,
                    email=test_user.email,
                    password=test_user.password,
                )
            )
        session.commit()

        def override_get_db() -> Generator:
            yield session

        app.dependency_overrides[get_db] = override_get_db
        yield session


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Returns a non-authorized test client for the API"""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    yield TestData.parse_file("test_api/test_data.json")


@pytest.fixture
def headers(
    client: TestClient,
    test_data: TestData,
    db,
) -> Generator[dict[str, str], None, None]:
    """Returns an authorized test client for the API"""
    user = test_data.test_users[0]
    response = client.post(
        "/api/auth/login",
        data={
            "username": user.username,
            "password": user.password,
        },
    )
    assert response.status_code == 200
    token = s.Token.parse_obj(response.json())

    yield dict(Authorization=f"Bearer {token.access_token}")
