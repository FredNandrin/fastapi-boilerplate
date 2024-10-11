from tests.client import client

def test_home():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"message": "FastApi is running"}
