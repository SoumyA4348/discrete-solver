import sys
import os
import pytest
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock joblib before importing app to avoid loading the real model
with patch('joblib.load') as mock_load:
    mock_load.return_value = MagicMock()
    from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_solve_route_success(client):
    with patch('app.solver_service.solve_question') as mock_solve:
        mock_solve.return_value = {
            "operation": "combinations",
            "answer": 10,
            "n": 5,
            "r": 3
        }
        response = client.post('/solve', 
                               data=json.dumps({"question": "Choose 3 from 5"}),
                               content_type='application/json')
        assert response.status_code == 200
        data = response.get_json()
        assert data["answer"] == 10
        assert data["operation"] == "combinations"

def test_solve_route_invalid_json(client):
    response = client.post('/solve', data="not json", content_type='application/json')
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_solve_route_empty_question(client):
    response = client.post('/solve', 
                           data=json.dumps({"question": ""}),
                           content_type='application/json')
    assert response.status_code == 400
    assert "error" in response.get_json()
