import requests

# Define the endpoint and payload
url = "http://127.0.0.1:5000/gds"
payload = {
    "demand_text": "Claim details including medical specials and pain/suffering.",
    "supporting_docs": "Details from demand package."
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())