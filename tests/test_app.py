import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

def test_signup_duplicate():
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Should not fail, but participant will be duplicated
    response = client.get("/activities")
    data = response.json()
    assert data[activity]["participants"].count(email) >= 1
