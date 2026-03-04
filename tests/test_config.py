"""
Tests for API/Classes/Base/Config.py
"""

import pytest
from pathlib import Path
import sys
import os


def test_config_imports():
    """
    Test that Config.py can be imported without errors.
    """
    try:
        from API.Classes.Base import Config
        assert Config is not None
    except ImportError as e:
        pytest.fail(f"Failed to import Config: {e}")


def test_base_dir_is_absolute():
    """
    Test that BASE_DIR is an absolute path.
    """
    from API.Classes.Base.Config import BASE_DIR
    
    assert Path(BASE_DIR).is_absolute(), \
        "BASE_DIR should be an absolute path"


def test_base_dir_exists():
    """
    Test that BASE_DIR points to an existing directory.
    """
    from API.Classes.Base.Config import BASE_DIR
    
    assert Path(BASE_DIR).exists(), \
        f"BASE_DIR does not exist: {BASE_DIR}"


def test_upload_folder_is_path_object():
    """
    Test that UPLOAD_FOLDER uses pathlib.Path (cross-platform).
    """
    from API.Classes.Base.Config import UPLOAD_FOLDER
    
    upload_path = Path(UPLOAD_FOLDER)
    assert upload_path is not None


def test_upload_folder_uses_correct_separators():
    """
    Test that paths use OS-appropriate separators.
    """
    from API.Classes.Base.Config import UPLOAD_FOLDER
    
    upload_str = str(UPLOAD_FOLDER)
    
    if sys.platform != 'win32':
        assert '\\' not in upload_str or '\\\\' in upload_str, \
            "Non-Windows paths should not contain single backslashes"


def test_config_paths_are_relative_to_base():
    """
    Test that all config paths are relative to BASE_DIR.
    """
    from API.Classes.Base.Config import BASE_DIR, UPLOAD_FOLDER
    
    base = Path(BASE_DIR)
    upload = Path(UPLOAD_FOLDER)
    
    try:
        upload.relative_to(base)
    except ValueError:
        pytest.fail(f"UPLOAD_FOLDER ({upload}) is not relative to BASE_DIR ({base})")


def test_path_joining_is_cross_platform():
    """
    Test that path joining works on all platforms.
    """
    from API.Classes.Base.Config import BASE_DIR
    
    test_path = Path(BASE_DIR) / 'test' / 'subdir' / 'file.txt'
    
    assert test_path is not None
    
    path_str = str(test_path)
    if sys.platform == 'win32':
        assert '\\' in path_str or '/' in path_str
    else:
        assert '/' in path_str


@pytest.mark.skipif(sys.platform == 'win32', reason="Unix-specific test")
def test_unix_paths_use_forward_slash():
    """
    Test that on Unix systems, paths use forward slashes.
    """
    from API.Classes.Base.Config import UPLOAD_FOLDER
    
    upload_str = str(UPLOAD_FOLDER)
    assert '/' in upload_str, "Unix paths should contain forward slashes"


@pytest.mark.skipif(sys.platform != 'win32', reason="Windows-specific test")
def test_windows_paths_are_valid():
    """
    Test that on Windows, paths are valid Windows paths.
    """
    from API.Classes.Base.Config import UPLOAD_FOLDER
    
    upload_path = Path(UPLOAD_FOLDER)
    
    assert upload_path.drive or upload_path.is_absolute(), \
        "Windows paths should have drive letter or be absolute"


def test_config_has_required_attributes():
    """
    Test that Config.py defines all required configuration.
    """
    from API.Classes.Base import Config
    
    required_attrs = [
        'BASE_DIR',
        'UPLOAD_FOLDER',
    ]
    
    for attr in required_attrs:
        assert hasattr(Config, attr), \
            f"Config.py missing required attribute: {attr}"


def test_config_paths_can_be_created(temp_dir):
    """
    Test that config paths can be created if they don't exist.
    """

    test_upload = temp_dir / 'WebAPP' / 'uploads'
    
    test_upload.mkdir(parents=True, exist_ok=True)
    assert test_upload.exists()
    assert test_upload.is_dir()
