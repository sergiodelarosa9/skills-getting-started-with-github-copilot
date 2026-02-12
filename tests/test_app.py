import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister():
    # Sign up a new participant
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json()["message"]

    # Try to sign up again (should fail)
    response = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"

    # Unregister participant
    response = client.delete("/activities/Chess Club/unregister?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered testuser@mergington.edu from Chess Club" in response.json()["message"]

    # Try to unregister again (should fail)
    response = client.delete("/activities/Chess Club/unregister?email=testuser@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up"
