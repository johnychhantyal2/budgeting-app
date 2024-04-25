from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# def test_create_admin_user():
#     # Test creating an admin user
#     response = client.post("/api/v1/admin/create", json={"username": "admin", "password": "Administrator123!"})
#     assert response.status_code == 200
#     assert response.json() == {"message": "Admin user created successfully"}

# def test_create_admin_user_invalid_data():
#     # Test creating an admin user with invalid data
#     response = client.post("/api/v1/admin/create", json={"username": "", "password": ""})
#     assert response.status_code == 422
#     assert response.json() == {"detail": [{"loc": ["body", "username"], "msg": "field required", "type": "value_error.missing"}, {"loc": ["body", "password"], "msg": "field required", "type": "value_error.missing"}]}
