"""
pytest configuration and shared fixtures for MUIOGO tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """
    Create a temporary directory for test files.
    
    Usage:
        def test_something(temp_dir):
            test_file = temp_dir / "test.txt"
            test_file.write_text("content")
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_case_data():
    """
    Provide sample case data for testing.
    
    Returns:
        dict: Sample case configuration
    """
    return {
        "case_name": "test_case",
        "description": "Test case for automated testing",
        "model_type": "CLEWS",
        "created_date": "2026-03-04"
    }


@pytest.fixture
def mock_config_paths(monkeypatch, temp_dir):
    """
    Mock Config.py paths to use temporary directory.
    
    Usage:
        def test_upload(mock_config_paths):
            # UPLOAD_FOLDER now points to temp directory
            from API.Classes.Base.Config import UPLOAD_FOLDER
    """
    # This will be used when we test Config.py
    monkeypatch.setenv("MUIOGO_TEST_MODE", "true")
    monkeypatch.setenv("MUIOGO_TEST_DIR", str(temp_dir))
    return temp_dir
