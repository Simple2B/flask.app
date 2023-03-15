from flask.testing import FlaskClient
from tests.utils import login, register


def test_list(client: FlaskClient):
    register("sam")
    response = login(client, "sam")
    assert b"Login successful." in response.data
    response = client.get("/list")
    assert response
    assert response.status_code == 200
