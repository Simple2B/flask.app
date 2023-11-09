import pytest
from fastapi.testclient import TestClient
from app import schema as s
from config import config
from .test_data import TestData

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_auth(db, client: TestClient, test_data: TestData):
    TEST_USERNAME = test_data.test_users[0].username
    TEST_PASSWORD = test_data.test_users[0].password
    res = client.post(
        "api/auth/token", json={"username": TEST_USERNAME, "password": TEST_PASSWORD}
    )
    assert res.status_code == 200
    token = s.Token.model_validate(res.json())
    assert token.access_token
    assert token.token_type == "bearer"
    header = dict(Authorization=f"Bearer {token.access_token}")
    res = client.get("api/users/me", headers=header)
    assert res.status_code == 200
