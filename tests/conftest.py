"""
Pytest configuration and shared fixtures for MUIOGO tests.
"""

import sys
from pathlib import Path

import pytest

# Add API directory to Python path for imports
API_DIR = Path(__file__).parent.parent / "API"
sys.path.insert(0, str(API_DIR))


@pytest.fixture
def temp_case_dir(tmp_path):
    """Create a temporary case directory with minimal structure."""
    case_dir = tmp_path / "test_case"
    case_dir.mkdir()
    
    # Create minimal Parameters.json
    params_file = case_dir / "Parameters.json"
    params_file.write_text('{"REGION": ["R1"], "YEAR": [2020, 2021]}')
    
    return case_dir


@pytest.fixture
def mock_solver_binary(tmp_path):
    """Create a mock solver binary for testing."""
    def _create_solver(name="glpsol", subdir=None):
        if subdir:
            solver_dir = tmp_path / subdir
            solver_dir.mkdir(parents=True, exist_ok=True)
        else:
            solver_dir = tmp_path
        
        solver_path = solver_dir / name
        solver_path.touch()
        solver_path.chmod(0o755)  # Make executable
        
        return solver_path
    
    return _create_solver


@pytest.fixture
def clean_env(monkeypatch):
    """Clean solver-related environment variables."""
    monkeypatch.delenv("SOLVER_GLPK_PATH", raising=False)
    monkeypatch.delenv("SOLVER_CBC_PATH", raising=False)
    return monkeypatch
