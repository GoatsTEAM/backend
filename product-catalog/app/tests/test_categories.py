import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_categories():
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
