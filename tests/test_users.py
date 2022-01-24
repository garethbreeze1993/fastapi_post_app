import pytest
from jose import jwt

from app.config import settings
from app.schemas import UserResponse, Token


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == "Welcome to my application!!!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post('/users/', json={"email": "moose@gmail.com", "password": "password123"})
    new_user = UserResponse(**res.json())
    assert new_user.email == "moose@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    user_id = payload.get('user_id')
    assert res.status_code == 200
    assert user_id == test_user['id']
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize("email, password, status_code", [
    ('moose@gmail.com', 'wrong password', 403),
    ('wrong_email@gmail.com', 'wrong password', 403),
    ('moose@gmail.com', None, 422),
    ('wrong_email@gmail.com', 'password123', 403),
    (None, 'password123', 422)])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})
    assert res.status_code == status_code
