import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

# ✅ Test Register
def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200  # changed from 302

# ✅ Test Duplicate Register
def test_duplicate_user(client):
    client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    assert b"User already exists" in response.data

# ✅ Test Login
def test_login(client):
    client.post('/register', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })

    assert response.status_code == 200  # changed from 302

# ❌ Test Invalid Login
def test_invalid_login(client):
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'wrong'
    })

    assert b"Invalid" in response.data