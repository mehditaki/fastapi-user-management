import pytest
from fastapi.testclient import TestClient

from fastapi_user_management.app import (
    app,  # Assuming your FastAPI app instance is named app
)


@pytest.fixture
def client():
    """Create a FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# Add more test functions for other endpoints as needed
