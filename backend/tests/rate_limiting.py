import requests
from time import sleep

# Replace with your actual endpoint
url = "http://127.0.0.1:8000/v1/transactions"

# Replace 'your_token_here' with your actual bearer token
bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdXBlcnVzZXIxIiwiZXhwIjoxNzEyMTEyODc3fQ.8iWxFW2ZSgf6Q_uiWPfm4MyF23iixBsjW_KqO7ycpec"
headers = {
    "Authorization": f"Bearer {bearer_token}"
}

# Replace 5 with your actual rate limit
for i in range(15):
    response = requests.get(url, headers=headers)  # Include headers in the request
    print(f"Request {i+1}: Status Code: {response.status_code}")
    if response.status_code == 429:
        print("Rate limit exceeded as expected.")
        break
# Wait for the rate limit window to reset
sleep(60)  # Adjust based on your rate limit window

# Test after rate limit window has reset
response = requests.get(url, headers=headers)  # Include headers in the request
print(f"After waiting: Status Code: {response.status_code}")
