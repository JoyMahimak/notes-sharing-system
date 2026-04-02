import pytest
from app import app, db, Note

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200


def test_upload_note(client):
    data = {
        'title': 'Test Note'
    }

    response = client.post('/upload', data=data)
    assert response.status_code == 302  # redirect after upload