from fastapi.testclient import TestClient

from src.app import app
from src import app as app_module

client = TestClient(app)


def test_unregister_participant_from_activity():
    activity_name = "Soccer Club"
    app_module.activities[activity_name]["participants"] = []

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email=student@example.com"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/unregister?email=student@example.com"
    )
    assert delete_response.status_code == 200
    assert "student@example.com" not in app_module.activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    app_module.activities[activity_name]["participants"] = ["already@mergington.edu"]

    response = client.post(
        f"/activities/{activity_name}/signup?email=already@mergington.edu"
    )

    assert response.status_code == 400
