import json
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_version(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_test_redis_connection(client):
    response = client.get("/test-redis")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "value" in response.json()
    assert response.json()["message"] == "Redis connection and operation successful"
    assert response.json()["value"] == "success"