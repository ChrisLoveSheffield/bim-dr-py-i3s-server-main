from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_slpk_page():
    response = client.get("/")
    assert response.status_code == 200
