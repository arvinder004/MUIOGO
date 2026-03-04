"""
Tests for file operations to ensure cross-platform compatibility.
Tests file reading, writing, and path handling.
"""

import pytest
from pathlib import Path


def test_file_write_and_read(temp_dir):
    """
    Test basic file write and read operations.
    """
    test_file = temp_dir / "test.txt"
    content = "Hello, MUIOGO!"
    
    test_file.write_text(content, encoding='utf-8')
    
    read_content = test_file.read_text(encoding='utf-8')
    
    assert read_content == content


def test_file_write_with_subdirectories(temp_dir):
    """
    Test file operations with nested directories.
    """
    nested_file = temp_dir / "level1" / "level2" / "test.txt"
    
    nested_file.parent.mkdir(parents=True, exist_ok=True)
    
    nested_file.write_text("nested content", encoding='utf-8')
    
    assert nested_file.exists()
    assert nested_file.read_text(encoding='utf-8') == "nested content"


def test_path_with_spaces(temp_dir):
    """
    Test handling paths with spaces
    """
    spaced_dir = temp_dir / "folder with spaces"
    spaced_dir.mkdir()
    
    test_file = spaced_dir / "file with spaces.txt"
    test_file.write_text("content", encoding='utf-8')
    
    assert test_file.exists()
    
    assert test_file.read_text(encoding='utf-8') == "content"


def test_relative_path_resolution(temp_dir):
    """
    Test resolving relative paths to absolute paths.
    """
    test_file = temp_dir / "test.txt"
    test_file.write_text("content", encoding='utf-8')
    
    relative = Path("test.txt")
    
    absolute = (temp_dir / relative).resolve()
    
    assert absolute.is_absolute()
    assert absolute.exists()


def test_path_comparison_cross_platform(temp_dir):
    """
    Test that path comparison works across platforms.
    """

    path1 = temp_dir / "test.txt"
    path2 = temp_dir / "test.txt"
    
    assert path1 == path2
    
    assert path1.resolve() == path2.resolve()
