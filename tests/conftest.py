import pytest
from flask.testing import FlaskClient

from app import create_app, db
from app import models as m
from tests.utils import register


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        register()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


@pytest.fixture
def populate(client: FlaskClient):
    NUM_TEST_USERS = 100
    for i in range(NUM_TEST_USERS):
        m.User(
            username=f"user{i+1}",
            email=f"user{i+1}@mail.com",
            password="password",
        ).save(False)
    db.session.commit()
    yield client
