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
    # assert response.status_code == 200
    return response.json().get("access_token", "")


@pytest.fixture
def auth_header(client: TestClient) -> dict:
    """Get authentication header for test requests."""
    # Replace these with valid credentials from your test database
    username = "admin@mail.com"
    password = "admin"
    token = get_auth_token(client, username, password)
    return {"Authorization": f"Bearer {token}"}


def test_read_users(client: TestClient, db: Session, auth_header: dict):
    """Test reading all users."""
    response = client.get("/admin/user", headers=auth_header)
    assert response.status_code == 200
    users_data = response.json()
    assert isinstance(users_data, list)


def test_create_user(client: TestClient, db: Session, auth_header: dict):
    """Test creating a new user."""
    new_user = {
        "fullname": "Riez",
        "username": "rinchez@citadel.com",
        "phone_number": "9123456789",
        "status": "active",
        "roles": [],
        "password": "Wubba--Dub-Dub",
        "last_login": "2023-12-12",
    }
    response = client.post("/admin/user", json=new_user, headers=auth_header)
    assert response.status_code == 200


def test_delete_user(client: TestClient, db: Session, auth_header: dict):
    """Test deleting a user."""
    username_to_delete = (  # Ensure this user exists before running the test
        "rinchez@citadel.com"
    )
    response = client.delete(
        f"/admin/user?username={username_to_delete}", headers=auth_header
    )
    assert response.status_code == 200


def test_user_not_found(client: TestClient, auth_header: dict):
    """Test user not found scenario."""
    non_existent_username = "nonexistent@mail.com"
    response = client.delete(
        f"/admin/user?username={non_existent_username}", headers=auth_header
    )
    assert response.status_code == 404


def test_access_denied(client: TestClient, auth_header: dict):
    """Test access denied for non-admin users."""
    # You need to have a non-admin user in your test database
    non_admin_auth_header = {
        "Authorization": f"Bearer {get_auth_token(client, 'user@mail.com', 'password')}"
    }
    response = client.get("/admin/user", headers=non_admin_auth_header)
    assert response.status_code == 401
