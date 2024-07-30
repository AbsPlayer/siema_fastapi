from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    # test main page
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"ping": "pong"}

    # test non exist url
    response = client.get("/url")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not Found"}
