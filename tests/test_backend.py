import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import FastAPI TestClient with a different approach
from fastapi.testclient import TestClient

# Import app after setting up the environment to avoid naming conflicts
from backend.main import app

client = TestClient(app)

def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Fewfinder API"}

def test_available_routes():
    """Test to see what routes are actually available"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_search_route_empty_query():
    response = client.post("/api/search", json={"question": ""})
    assert response.status_code == 200
    assert "video_url" in response.json()

def test_search_route_valid_query():
    response = client.post("/api/search", json={"question": "How long do cats live?"})
    assert response.status_code == 200
    data = response.json()
    assert "video_url" in data
    assert "transcript_text" in data
    assert "start_time" in data
