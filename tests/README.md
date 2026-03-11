# MUIOGO Test Suite

This directory contains automated tests for MUIOGO.

## Running Tests

### Run all tests
```bash
pytest tests/
```

### Run specific test file
```bash
pytest tests/test_solver_discovery.py
```

### Run with coverage
```bash
pytest tests/ --cov=API --cov-report=html
```

### Run with verbose output
```bash
pytest tests/ -v
```

### Run specific test class or function
```bash
pytest tests/test_solver_discovery.py::TestResolveSolverFolder
pytest tests/test_solver_discovery.py::TestResolveSolverFolder::test_resolve_from_env_var_directory
```

## Test Structure

- `conftest.py` - Shared fixtures and pytest configuration
- `test_solver_discovery.py` - Tests for platform-independent solver discovery

## Test Coverage

Current test coverage focuses on:

### Solver Discovery (`test_solver_discovery.py`)
- ✅ Platform-specific binary name generation (Windows .exe handling)
- ✅ Finding solver binaries in directories (recursive and non-recursive)
- ✅ Three-tier resolution priority (env var → PATH → bundled)
- ✅ Environment variable handling (with quotes, paths, files)
- ✅ Error messages when solvers not found
- ✅ Caching behavior
- ✅ Cross-platform behavior

## Adding New Tests

1. Create a new test file: `test_<feature>.py`
2. Import necessary modules and fixtures from `conftest.py`
3. Organize tests into classes by functionality
4. Use descriptive test names: `test_<what>_<condition>_<expected>`
5. Add docstrings explaining what each test verifies

Example:
```python
class TestMyFeature:
    """Test my feature functionality."""
    
    def test_feature_with_valid_input_succeeds(self):
        """Should succeed when given valid input."""
        result = my_feature("valid")
        assert result == "expected"
```

## Continuous Integration

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Multiple platforms: Windows, macOS, Linux
- Multiple Python versions: 3.11+

## Test Requirements

Install test dependencies:
```bash
pip install pytest pytest-cov
```

Or use the development requirements:
```bash
pip install -r requirements-dev.txt  # If this file exists
```
