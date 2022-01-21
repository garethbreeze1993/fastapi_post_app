from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import get_db, Base

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
