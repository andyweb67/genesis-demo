import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_adjuster_questions():
    url = f"{BASE_URL}/adjuster"
    payload = {
        "adjuster_name": "Jane Smith",
        "liability_percentage": 80
    }
    response = requests.post(url, json=payload)

    # Check the status code
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Validate the response data
    response_data = response.json()
    assert response_data["message"] == "Adjuster Jane Smith assigned 80% liability."
    assert response_data["status"] == "Processed successfully."