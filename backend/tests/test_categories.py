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

# Test creating a category with authentication header
headers = {"Authorization": f"Bearer {token}"}

def test_create_category_endpoint():
    # Test creating a category
    response = client.post("/v1/categories/", json={"name": "Category 1", "budgeted_amount": 0, "budgeted_limit": 0, "color_code": "blue", "description": "", "icon": ""}, headers=headers)
    print(response.json())
    assert response.status_code == 200

def test_create_category_endpoint_invalid_data():
    # Test creating a category with invalid data
    response = client.post("/v1/categories/", json={"testname": ""}, headers=headers)
    assert response.status_code == 422
    print(response.json())

def test_read_categories():
    # Test reading categories
    response = client.get("/v1/categories/", headers=headers)
    assert response.status_code == 200

def test_read_category():
    # Test reading a category
    response = client.get("/v1/categories/36/", headers=headers)
    assert response.status_code == 200

def test_read_category_not_found():
    # Test reading a category that does not exist
    response = client.get("/v1/categories/2/", headers=headers)
    assert response.status_code == 404

def test_update_category_endpoint():
    # Test updating a category
    response = client.put("/v1/categories/36/", json={"name": "Category 1 Updated"}, headers=headers)
    assert response.status_code == 200