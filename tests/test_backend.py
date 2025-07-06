import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Fewfinder backend is running."}

def test_search_route_empty_query():
    response = client.post("/search", json={"query": ""})
    assert response.status_code == 200
    assert "results" in response.json()

def test_search_route_valid_query():
    response = client.post("/search", json={"query": "How long do cats live?"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
