from flask.testing import FlaskClient
from app import models as m
from tests.utils import login


def test_list(populate: FlaskClient):
    login(populate)
    response = populate.get("/list")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    users = m.User.query.limit(11).all()
    assert len(users) == 11
    for user in users[:10]:
        assert user.username in html
    assert users[10].username not in html
