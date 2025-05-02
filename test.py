from fastapi.testclient import TestClient
from app.main import app


def test_read_slpk_page():
    response = client.get("/")
    assert response.status_code == 200


if __name__ == "__main__":
    client = TestClient(app)
    test_read_slpk_page()
    print("All tests passed.")
