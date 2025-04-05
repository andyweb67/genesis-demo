import requests

# Define the endpoint and payload
url = "http://127.0.0.1:5000/adjuster"
payload = {
    "adjuster_name": "John Doe",
    "liability_percentage": 80
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response from the server
print("Status Code:", response.status_code)
print("Response JSON:", response.json())