from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_products():
    response = client.get("/products/")
    assert response.status_code == 200
