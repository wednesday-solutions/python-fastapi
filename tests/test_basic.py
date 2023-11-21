
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"response": "service up and running..!"}


def test_example():
    assert 1 == 1
