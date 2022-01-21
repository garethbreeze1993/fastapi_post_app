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
