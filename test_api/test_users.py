import pytest

from fastapi.testclient import TestClient

from app import schema as s
from config import config

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_me(
    client: TestClient,
    headers: dict[str, str],
):
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
    user = s.User.parse_obj(response.json())
    assert user.username == "user1"
