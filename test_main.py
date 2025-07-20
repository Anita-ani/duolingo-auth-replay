# test_app.py
from fastapi.testclient import TestClient
from app import app  # Adjust the import to match your structure

client = TestClient(app)

def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
