import requests
import json
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()
test_user = os.getenv("TEST_USER");
test_password = os.getenv("TEST_PASSWORD");

# Define the base URL of your FastAPI application
base_url = "http://localhost:8000"

# Call login endpoint to get the token
response = requests.post(
    f"{base_url}/v1/auth/login",
    data=json.dumps({"username": test_user, "password": test_password}),
)

# Check if the request was successful

# Use the token for subsequent requests
token = response.json().get("access_token")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
}

const_string = "<string>";

# Define the data for a new category
category_data = {
  "name": "test category",
  "budgeted_amount": 0,
  "budgeted_limit": 0,
  "description": const_string,
  "icon": const_string
}

# Send a POST request to create a new category
response = requests.post(
    f"{base_url}/v1/categories/",
    headers=headers,
    data=json.dumps(category_data),
)

# Check if the request was successful
if response.status_code == 200:
    print("Category created successfully")
else:
    print("Failed to create category")

# Send a GET request to retrieve all categories
response = requests.get(
    f"{base_url}/v1/categories/",
    headers=headers,
)

# Check if the request was successful
if response.status_code == 200:
    categories = response.json()
    print("Categories retrieved successfully")
    for category in categories:
        print(category)
else:
    print("Failed to retrieve categories")


# Send a GET request to get all transactions
response = requests.get(
    f"{base_url}/v1/transactions/",
    headers=headers,
)

# Check if the request was successful
if response.status_code == 200:
    transactions = response.json()
    print("Transactions retrieved successfully")
    for transaction in transactions:
        print(transaction)
else:
    print("Failed to retrieve transactions")