def test_get_me():
    from config import config

    CFG = config("testing")
    assert CFG.IS_API
