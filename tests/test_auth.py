import re
from flask_mail import Message
from flask import url_for

from app import mail
from app import models as m
from tests.utils import register, login, logout


def test_auth_pages(client):
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302


def test_register(client):
    TEST_EMAIL = "sam@test.com"

    with mail.record_messages() as outbox:

        response = client.post(
            "/register",
            data=dict(
                username="sam",
                email=TEST_EMAIL,
                password="password",
                password_confirmation="password",
            ),
            follow_redirects=True,
        )

        assert (
            b"Registration successful. Checkout you email for confirmation!."
            in response.data
        )

        user = m.User.query.filter_by(email=TEST_EMAIL).first()
        assert user

        assert len(outbox) == 1
        letter: Message = outbox[0]
        assert letter.subject == "New password"
        assert "Confirm registration" in letter.html
        assert user.unique_id in letter.html
        html: str = letter.html
        pattern = r"https?:\/\/[\w\d\.-]+\/activated\/[\w\d-]{36}"
        urls = re.findall(pattern, html)
        assert len(urls) == 1
        url = urls[0]
        response = client.get(url)
        assert response.status_code == 302
        response.location == url_for("main.index")
        user: m.User = m.User.query.filter_by(email=TEST_EMAIL).first()
        assert user
        assert user.activated


def test_login_and_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data
    register("sam")
    response = login(client, "sam")
    assert b"Login successful." in response.data
    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data
    # Incorrect login credentials should fail.
    response = login(client, "sam", "wrongpassword")
    assert b"Wrong user ID or password." in response.data
    # Correct credentials should login
    response = login(client, "sam")
    assert b"Login successful." in response.data
