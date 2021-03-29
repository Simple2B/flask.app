from app.models import User


def register(username, email="username@test.com", password="password"):
    user = User(username=username, email=email, password=password)
    user.save()
    return user.id


def login(client, username, password="password"):
    return client.post(
        "/login", data=dict(user_id=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
