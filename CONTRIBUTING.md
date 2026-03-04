# Contributing to MUIOGO

Thanks for contributing!

## Before starting

1. Read `README.md`, `docs/GSoC-2026.md`, `docs/ARCHITECTURE.md`, and
   `docs/DOCS_POLICY.md`
2. Create or use an existing issue before starting implementation work
3. Create a feature branch from `main` for that issue
4. Confirm acceptance criteria in the issue so review can be objective

## Scope and repository boundaries

- This repo is downstream from `OSeMOSYS/MUIO` and must be deliverable on its own
- Do not block work here on upstream changes
- Upstream collaboration is encouraged, but this repo needs independent completion
- `MUIO-Mac` may be referenced, but `MUIOGO` targets platform-independent operation

## Issue Prioritization

We use the following priority system:
- High: issues that should be worked on ASAP
- Medium: important issues
- Low: issues that may be important but that can wait

❗️Priorities are assigned by maintainers.

## Workflow

1. Start from an issue
2. Create a feature branch from `main`
3. Keep branch changes scoped to one issue or one tightly related set of issues
4. Include tests or validation steps whenever behavior changes
5. Update docs for any setup, architecture, or workflow change
6. Open a PR into `EAPD-DRB/MUIOGO:main` using the repository PR template

## Required branching rule

Every contribution must use:

- an issue for scope and acceptance criteria
- a feature branch for implementation

Suggested branch format:

- `feature/<issue-number>-short-description`

## Communication model

This project uses event-driven updates (no weekly cadence requirement).
Post updates when one of these events occurs:

- Work started
- Blocked longer than 48 hours
- PR opened
- PR ready for review
- Milestone completed

## PR requirements

- Clear description of what changed and why
- Link to issue(s)
- Validation evidence:
  - test output, or
  - reproducible manual verification steps
- Docs updated when needed
- No unrelated refactors in the same PR
- PR target is `EAPD-DRB/MUIOGO:main` (not upstream `OSeMOSYS/MUIO`)

## Definition of done

A task is done when:

1. Acceptance criteria in the issue are met
2. Code and docs are updated together
3. Reviewer feedback is resolved
4. Changes are merged to `EAPD-DRB/MUIOGO:main`

---

## Development Setup

### 1. Clone the repository
```bash
git clone https://github.com/EAPD-DRB/MUIOGO.git
cd MUIOGO
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running Tests

We use pytest for automated testing to ensure cross-platform compatibility.

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=API --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/test_config.py
```

### Run specific test function
```bash
pytest tests/test_config.py::test_base_dir_is_absolute
```

### Run tests matching a pattern
```bash
pytest -k "test_path"
```

### Run verbose output
```bash
pytest -v
```

### Run with print statements visible
```bash
pytest -s
```

---

## Writing Tests

### Test Structure
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use fixtures from `conftest.py`

### Using Fixtures
Fixtures are defined in `tests/conftest.py` and automatically available:

```python
def test_with_temp_directory(temp_dir):
    """
    temp_dir fixture provides a temporary directory.
    """
    test_file = temp_dir / "file.txt"
    test_file.write_text("content")
    assert test_file.exists()

def test_with_sample_data(sample_case_data):
    """
    sample_case_data fixture provides test case data.
    """
    assert sample_case_data["case_name"] == "test_case"
    assert sample_case_data["model_type"] == "CLEWS"
```

### Test Markers
Use markers to categorize tests:

```python
@pytest.mark.slow
def test_long_running_operation():
    """
    Mark slow tests to skip during quick test runs.
    """
    pass

@pytest.mark.integration
def test_full_workflow():
    """
    Mark integration tests separately from unit tests.
    """
    pass

@pytest.mark.skipif(sys.platform == 'win32', reason="Unix-specific test")
def test_unix_only_feature():
    """
    Skip tests on specific platforms.
    """
    pass
```

Run tests by marker:
```bash
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Run only integration tests
```

---

## Continuous Integration

All PRs are automatically tested via GitHub Actions on:
- **Operating Systems:** Ubuntu, macOS, Windows
- **Python Versions:** 3.9, 3.10, 3.11

### CI Workflow
1. Push commits to your feature branch
2. GitHub Actions automatically runs tests on all platforms
3. Check the "Actions" tab for results
4. Green checkmark = all tests passed on all platforms
5. Red X = tests failed, click for details

### Before Pushing
Ensure tests pass locally:
```bash
pytest
```

If tests fail in CI but pass locally, it's likely a platform-specific issue. Check the CI logs to see which platform failed.

---

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused and small (single responsibility)
- Use type hints where appropriate
- Use `pathlib.Path` for file paths (cross-platform compatibility)
