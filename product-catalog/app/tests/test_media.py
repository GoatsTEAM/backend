from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_media_crud():
    product_id = 1
    media_data = {
        "storage_key": "test_key",
        "media_type": "image",
        "position": 0,
        "metadata": {"resolution": "1920x1080", "size_kb": 450}
    }
    response = client.post(f"/api/v1/products/{product_id}/media", json=media_data)
    assert response.status_code in (200, 201)
    media_id = response.json()["media_id"]
    response = client.get(f"/api/v1/products/{product_id}/media")
    assert response.status_code == 200
    response = client.delete(f"/api/v1/media/{media_id}")
    assert response.status_code == 200
