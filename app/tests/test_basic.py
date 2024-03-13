from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/api/home")
    assert response.status_code == 200
    assert response.json() == {"response": "service up and running..!"}


def test_example():
    assert 1 == 1


#
def test_circuit_breaker():
    # Send enough requests to trip the circuit breaker
    for _ in range(10):
        client.get("/api/home/external-service")

    # After the circuit breaker trips, this request should fail
    response = client.get("/api//home/external-service")
    assert response.status_code == 429
    assert response.json()["error"] == "Too Many Requests"
