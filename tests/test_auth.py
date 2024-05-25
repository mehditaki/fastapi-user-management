import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fastapi_user_management.app import app
from fastapi_user_management.core.database import get_db


@pytest.fixture
def client():
    """Create a FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db() -> Session:
    """Create a database session for testing."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()


def test_login(client: TestClient, db: Session):
    """Test user login."""
    form_data = {"username": "admin@mail.com", "password": "admin"}
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data


def test_invalid_credentials(client: TestClient, db: Session):
    """Test login with invalid credentials."""
    form_data = {"username": "invalid", "password": "invalid"}
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 401


def test_invalid_token(client: TestClient):
    """Test accessing protected route with invalid token."""
    response = client.get(
        "/admin/user", headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401


def test_inactive_user(client: TestClient, db: Session):
    """Test accessing protected route with inactive user."""
    form_data = {"username": "inactive@mail.com", "password": "inactive"}
    client.post("/auth/token", data=form_data)
    response = client.get(
        "/admin/user", headers={"Authorization": "Bearer inactive_user_token"}
    )
    assert response.status_code == 401
