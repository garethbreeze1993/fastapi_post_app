from fastapi.testclient import TestClient
import pytest

from app import models
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token

from tests.database import TestingSessionLocal, engine

# THIS FILE IS FOR DEFINING FIXTURES WHICH PYTEST CAN AUTOMATICALLY USE IN TEST FILES BY PASSING IN THE EXACT NAME OF
# THE FIXTURE TO THE TEST FUNC PARAMTER
# i.e. @pytest.fixture
#           def foo():
#               return 'foo'
#
#     def test_bar(foo):
#          assert foo == 'foo'


@pytest.fixture
def session():
    # creates the database tables before running the test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):

    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)  # gives us the test client so we can run our tests

    # after test has run we can drop all tables in our database
    # If want to look at tables after test move line below above the create_all call in session fixture
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(client):
    user_data = {"email": "moose@gmail.com", "password": "password123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = dict(password=user_data['password'], **res.json())
    return new_user


@pytest.fixture
def token(test_user):
    access_token = create_access_token(data=dict(user_id=test_user['id']))
    return access_token


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({'Authorization': f'Bearer {token}'})
    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{'title': 'title 1', 'content': 'content_1', 'owner_id': test_user['id']},
                  {'title': 'title 2', 'content': 'content_2', 'owner_id': test_user['id']},
                  {'title': 'title 3', 'content': 'content_3', 'owner_id': test_user['id']}]

    for post in posts_data:
        model_post = models.Post(**post)
        session.add(model_post)

    session.commit()

    post_query = session.query(models.Post)\
        .all()

    return post_query
