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


def get_auth_token(client: TestClient, username: str, password: str) -> str:
    """Authenticate and return a token."""
    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_header(client: TestClient) -> dict:
    """Get authentication header for test requests."""
    # Replace these with valid credentials from your test database
    username = "admin@mail.com"
    password = "admin"
    token = get_auth_token(client, username, password)
    return {"Authorization": f"Bearer {token}"}


def test_read_user_profile_by_id(client: TestClient, db: Session, auth_header: dict):
    """Test reading a user's profile by user ID."""
    user_id = 1  # Replace with a valid user ID
    response = client.get(f"/user?id={user_id}", headers=auth_header)
    assert response.status_code == 200
    user_data = response.json()
    assert "username" in user_data


def test_read_user_profile_by_username(
    client: TestClient, db: Session, auth_header: dict
):
    """Test reading a user's profile by username."""
    username = "admin@mail.com"  # Replace with a valid username
    response = client.get(f"/user?username={username}", headers=auth_header)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == username


def test_user_not_found(client: TestClient, auth_header: dict):
    """Test user profile not found scenario."""
    non_existent_user_id = 9999
    response = client.get(f"/user?id={non_existent_user_id}", headers=auth_header)
    assert response.status_code == 404


def test_internal_server_error(client: TestClient, monkeypatch, auth_header: dict):
    """Test internal server error scenario."""

    def mock_get_by_id(db, id):
        raise Exception("Mocked exception")

    monkeypatch.setattr("fastapi_user_management.crud.user.get_by_id", mock_get_by_id)
    response = client.get("/user?id=1", headers=auth_header)
    assert response.status_code == 500
