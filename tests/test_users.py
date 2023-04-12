from flask import current_app as app
from flask.testing import FlaskClient, FlaskCliRunner
from click.testing import Result
from app import models as m
from tests.utils import login


def test_list(populate: FlaskClient):
    login(populate)
    response = populate.get("/user/")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    users = m.User.query.limit(11).all()
    assert len(users) == 11
    for user in users[:10]:
        assert user.username in html
    assert users[10].username not in html

    populate.application.config["PAGE_LINKS_NUMBER"] = 6
    response = populate.get("/user/?page=6")
    assert response
    assert response.status_code == 200
    html = response.data.decode()
    assert "/user/?page=6" in html
    assert "/user/?page=3" in html
    assert "/user/?page=8" in html
    assert "/user/?page=10" not in html
    assert "/user/?page=2" not in html


def test_create_admin(runner: FlaskCliRunner):
    res: Result = runner.invoke(args=["create-admin"])
    assert "admin created" in res.output
    assert m.User.query.filter_by(username=app.config["ADMIN_USERNAME"]).first()


def test_populate_db(runner: FlaskCliRunner):
    TEST_COUNT = 56
    count_before = m.User.query.count()
    res: Result = runner.invoke(args=["db-populate", "--count", f"{TEST_COUNT}"])
    assert f"populated by {TEST_COUNT}" in res.stdout
    assert (m.User.query.count() - count_before) == TEST_COUNT
