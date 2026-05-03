import sys
import os
import pytest
from unittest.mock import MagicMock

# Add parent directory to path to import solver_service
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver_service import SolverService, extract_numbers

def test_extract_numbers():
    assert extract_numbers("How many ways to pick 3 from 5?") == [3, 5]
    assert extract_numbers("Three items from five items.") == [3, 5]
    assert extract_numbers("Twelve items or a dozen.") == [12, 12]
    assert extract_numbers("Zero items from ten.") == [0, 10]
    assert extract_numbers("No numbers here.") == []

def test_solver_service_permutations():
    mock_model = MagicMock()
    mock_model.predict.return_value = ["permutations"]
    service = SolverService(mock_model)
    
    result = service.solve_question("Pick 3 from 5 items")
    assert result["operation"] == "permutations"
    assert result["n"] == 5
    assert result["r"] == 3
    assert result["answer"] == 60

def test_solver_service_combinations():
    mock_model = MagicMock()
    mock_model.predict.return_value = ["combinations"]
    service = SolverService(mock_model)
    
    result = service.solve_question("Choose 2 from 4")
    assert result["operation"] == "combinations"
    assert result["n"] == 4
    assert result["r"] == 2
    assert result["answer"] == 6

def test_solver_service_large_numbers():
    mock_model = MagicMock()
    mock_model.predict.return_value = ["permutations"]
    service = SolverService(mock_model)
    
    with pytest.raises(ValueError, match="Numbers are too large"):
        service.solve_question("Pick 10001 from 20000")

def test_solver_service_no_model():
    service = SolverService(None)
    with pytest.raises(ValueError, match="ML model not loaded"):
        service.solve_question("Pick 3 from 5")

def test_solver_service_no_numbers():
    mock_model = MagicMock()
    mock_model.predict.return_value = ["permutations"]
    service = SolverService(mock_model)
    with pytest.raises(ValueError, match="No numbers found"):
        service.solve_question("How many ways?")
