import requests

# Mock claim data
mock_data = {
    "claim_id": "12345",
    "category": "Medical Specials",
    "attorney_demand": 12000,
    "adjuster_offer": 2000,
    "notes": "Re-aggravation of pre-existing condition"
}

# Send POST request to the Flask app
response = requests.post('http://127.0.0.1:5000/process_claim', json=mock_data)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
