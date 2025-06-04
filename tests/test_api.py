import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app import models

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "phone": "123-456-7890",
            "website": "test.com",
            "address": {
                "street": "Test Street",
                "suite": "Test Suite",
                "city": "Test City",
                "zipcode": "12345",
                "geo": {
                    "lat": "0",
                    "lng": "0"
                }
            },
            "company": {
                "name": "Test Company",
                "catchPhrase": "Test Phrase",
                "bs": "Test BS"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_login():
    # First register a user
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "password123",
            "phone": "123-456-7890",
            "website": "test.com",
            "address": {
                "street": "Test Street",
                "suite": "Test Suite",
                "city": "Test City",
                "zipcode": "12345",
                "geo": {
                    "lat": "0",
                    "lng": "0"
                }
            },
            "company": {
                "name": "Test Company",
                "catchPhrase": "Test Phrase",
                "bs": "Test BS"
            }
        }
    )
    
    # Then try to login
    response = client.post(
        "/auth/login",
        data={"username": "testuser2", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_users_unauthorized():
    response = client.get("/users")
    assert response.status_code == 401

def test_get_users_authorized():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser2", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Then try to get users with token
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_user():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser2", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    # Then try to update user
    response = client.put(
        "/users/2",  # Update user ID 2 (testuser2's own profile)
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Updated Name",
            "phone": "987-654-3210"
        }
    )
    assert response.status_code == 200

def test_delete_user():
    # First login to get token
    login_response = client.post(
        "/auth/login",
        data={"username": "testuser2", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    # Then try to delete user
    response = client.delete(
        "/users/2",  # Delete user ID 2 (testuser2's own profile)
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204 