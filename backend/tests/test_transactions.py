from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

# call login endpoint to get a valid JWT token using the test user from .env file
test_user = os.getenv("TEST_USER");
test_password = os.getenv("TEST_PASSWORD");
response = client.post("/v1/auth/login", json={"username": test_user, "password": test_password})
assert response.status_code == 200
assert "access_token" in response.json()
assert "refresh_token" in response.json()
token = response.json()["access_token"]
print("Response is:")
print(response.json())

# create authentication header with token
headers = {"Authorization": f"Bearer {token}"}

def test_create_transaction_endpoint():
    # Test creating a transaction
    response = client.post("/v1/transactions/", json={"Amount": 10, "Date": "2021-09-01", "Description": "Test transaction", "Note":"", "Location":"", "CategoryID":"", "Is_Income":0}, headers=headers)
    assert response.status_code == 200

def test_create_transaction_endpoint_invalid_data():
    # Test creating a transaction with invalid data
    response = client.post("/v1/transactions/", json={"amount": 10, "date": "2021-09-01", "description": "Test transaction", "type": "invalid"}, headers=headers)
    assert response.status_code == 422

def test_read_transactions():
    # Test reading transactions
    response = client.get("/v1/transactions/", headers=headers)
    assert response.status_code == 200

def test_read_transaction():
    # Test reading a transaction
    response = client.get("/v1/transactions/69/", headers=headers)
    assert response.status_code == 200

def test_read_transaction_not_found():
    # Test reading a transaction that does not exist
    response = client.get("/v1/transactions/100/", headers=headers)
    assert response.status_code == 404

def test_update_transaction_endpoint():
    # Test updating a transaction
    response = client.put("/v1/transactions/56/", json={"Amount": 20}, headers=headers)
    assert response.status_code == 200

def test_delete_transaction():
    # Test deleting a transaction
    response = client.delete("/v1/transactions/68/", headers=headers)
    assert response.status_code == 200

def test_delete_transaction_not_found():
    # Test deleting a transaction that does not exist
    response = client.delete("/v1/transactions/100/", headers=headers)
    assert response.status_code == 404

