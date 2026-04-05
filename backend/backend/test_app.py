import pytest
from app import app, db, Note
import io

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
        'title': 'Test Note',
        'file': (io.BytesIO(b"dummy content"), 'test.txt')  # ✅ FIX HERE
    }

    response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 302  # redirect after upload