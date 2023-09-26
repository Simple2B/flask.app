import pytest
from config import config

CFG = config("testing")


@pytest.mark.skipif(not CFG.IS_API, reason="API is not enabled")
def test_get_me():
    assert CFG.IS_API
