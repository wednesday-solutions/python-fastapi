from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_read_main():
    mock_rate_limit_middleware = MagicMock()
    with patch("app.middlewares.rate_limiter_middleware.RateLimitMiddleware", mock_rate_limit_middleware):
        response = client.get("/api/home")
        assert response.status_code in [200, 429]


def test_example():
    test_value1 = 1
    test_value2 = 1
    assert test_value1 == test_value2


#
def test_circuit_breaker():
    # Send enough requests to trip the circuit breaker
    for _ in range(10):
        client.get("/api/home/external-service")

    # After the circuit breaker trips, this request should fail
    response = client.get("/api//home/external-service")
    assert response.status_code == 429
