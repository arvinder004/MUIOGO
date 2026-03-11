"""
Tests for platform-independent solver discovery in OsemosysClass.

Tests the three-tier solver resolution:
1. Environment variable (SOLVER_GLPK_PATH, SOLVER_CBC_PATH)
2. System PATH via shutil.which
3. Bundled fallback in SOLVERs_FOLDER
"""

import os
import platform
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add API to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "API"))

from Classes.Case.OsemosysClass import Osemosys
from Classes.Base import Config


class TestSolverBinaryNames:
    """Test platform-specific binary name generation."""

    def test_unix_binary_names(self):
        """On Unix systems, should return just the binary name."""
        with patch('platform.system', return_value='Linux'):
            names = Osemosys._solver_binary_names('glpsol')
            assert names == ['glpsol']

    def test_windows_binary_names(self):
        """On Windows, should add .exe extension."""
        with patch('platform.system', return_value='Windows'):
            names = Osemosys._solver_binary_names('glpsol')
            assert 'glpsol.exe' in names
            assert 'glpsol' in names
            # .exe version should be first (higher priority)
            assert names[0] == 'glpsol.exe'

    def test_windows_binary_names_already_has_exe(self):
        """If binary already has .exe, don't duplicate."""
        with patch('platform.system', return_value='Windows'):
            names = Osemosys._solver_binary_names('glpsol.exe')
            # Should not have duplicate .exe
            assert names.count('glpsol.exe') == 1


class TestFindSolverBinary:
    """Test finding solver binaries in directories."""

    def test_find_binary_in_directory(self, tmp_path):
        """Should find binary in directory."""
        # Create a fake solver binary
        solver_dir = tmp_path / "solvers"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol"
        solver_binary.touch()

        result = Osemosys._find_solver_binary(solver_dir, "glpsol", recursive=False)
        assert result == solver_binary

    def test_find_binary_direct_file_path(self, tmp_path):
        """Should handle direct file path."""
        solver_binary = tmp_path / "glpsol"
        solver_binary.touch()

        result = Osemosys._find_solver_binary(solver_binary, "glpsol", recursive=False)
        assert result == solver_binary

    def test_find_binary_wrong_name(self, tmp_path):
        """Should return None if binary name doesn't match."""
        solver_binary = tmp_path / "cbc"
        solver_binary.touch()

        result = Osemosys._find_solver_binary(solver_binary, "glpsol", recursive=False)
        assert result is None

    def test_find_binary_nonexistent_path(self, tmp_path):
        """Should return None for nonexistent path."""
        nonexistent = tmp_path / "does_not_exist"
        result = Osemosys._find_solver_binary(nonexistent, "glpsol", recursive=False)
        assert result is None

    def test_find_binary_recursive(self, tmp_path):
        """Should find binary in subdirectories when recursive=True."""
        # Create nested structure
        solver_dir = tmp_path / "solvers" / "glpk" / "bin"
        solver_dir.mkdir(parents=True)
        solver_binary = solver_dir / "glpsol"
        solver_binary.touch()

        # Non-recursive should not find it
        result = Osemosys._find_solver_binary(tmp_path / "solvers", "glpsol", recursive=False)
        assert result is None

        # Recursive should find it
        result = Osemosys._find_solver_binary(tmp_path / "solvers", "glpsol", recursive=True)
        assert result == solver_binary

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
    def test_find_binary_windows_exe(self, tmp_path):
        """On Windows, should find .exe version."""
        solver_dir = tmp_path / "solvers"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol.exe"
        solver_binary.touch()

        result = Osemosys._find_solver_binary(solver_dir, "glpsol", recursive=False)
        assert result == solver_binary


class TestResolveSolverFolder:
    """Test the three-tier solver resolution logic."""

    def test_resolve_from_env_var_directory(self, tmp_path, monkeypatch):
        """Should resolve from environment variable pointing to directory."""
        solver_dir = tmp_path / "glpk_bin"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol"
        solver_binary.touch()

        monkeypatch.setenv("SOLVER_GLPK_PATH", str(solver_dir))

        result = Osemosys._resolve_solver_folder(
            env_var="SOLVER_GLPK_PATH",
            binary_name="glpsol",
            bundled_path=tmp_path / "bundled"
        )

        assert result == solver_dir

    def test_resolve_from_env_var_file(self, tmp_path, monkeypatch):
        """Should resolve from environment variable pointing to binary file."""
        solver_dir = tmp_path / "glpk_bin"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol"
        solver_binary.touch()

        # Point directly to the binary
        monkeypatch.setenv("SOLVER_GLPK_PATH", str(solver_binary))

        result = Osemosys._resolve_solver_folder(
            env_var="SOLVER_GLPK_PATH",
            binary_name="glpsol",
            bundled_path=tmp_path / "bundled"
        )

        assert result == solver_dir

    def test_resolve_from_env_var_with_quotes(self, tmp_path, monkeypatch):
        """Should handle environment variable with quotes."""
        solver_dir = tmp_path / "glpk_bin"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol"
        solver_binary.touch()

        # Set with quotes (common on Windows)
        monkeypatch.setenv("SOLVER_GLPK_PATH", f'"{solver_dir}"')

        result = Osemosys._resolve_solver_folder(
            env_var="SOLVER_GLPK_PATH",
            binary_name="glpsol",
            bundled_path=tmp_path / "bundled"
        )

        assert result == solver_dir

    def test_resolve_from_env_var_invalid_raises_error(self, tmp_path, monkeypatch):
        """Should raise RuntimeError if env var is set but binary not found."""
        monkeypatch.setenv("SOLVER_GLPK_PATH", str(tmp_path / "nonexistent"))

        with pytest.raises(RuntimeError) as exc_info:
            Osemosys._resolve_solver_folder(
                env_var="SOLVER_GLPK_PATH",
                binary_name="glpsol",
                bundled_path=tmp_path / "bundled"
            )

        assert "SOLVER_GLPK_PATH" in str(exc_info.value)
        assert "glpsol" in str(exc_info.value)

    def test_resolve_from_system_path(self, tmp_path, monkeypatch):
        """Should resolve from system PATH via shutil.which."""
        solver_dir = tmp_path / "system_bin"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol"

        # Clear env var
        monkeypatch.delenv("SOLVER_GLPK_PATH", raising=False)

        # Mock shutil.which to return our test binary
        with patch('shutil.which', return_value=str(solver_binary)):
            result = Osemosys._resolve_solver_folder(
                env_var="SOLVER_GLPK_PATH",
                binary_name="glpsol",
                bundled_path=tmp_path / "bundled"
            )

            assert result == solver_dir

    def test_resolve_from_bundled_fallback(self, tmp_path, monkeypatch):
        """Should fall back to bundled solver."""
        bundled_dir = tmp_path / "bundled" / "GLPK" / "bin"
        bundled_dir.mkdir(parents=True)
        solver_binary = bundled_dir / "glpsol"
        solver_binary.touch()

        # Clear env var
        monkeypatch.delenv("SOLVER_GLPK_PATH", raising=False)

        # Mock shutil.which to return None (not on PATH)
        with patch('shutil.which', return_value=None):
            result = Osemosys._resolve_solver_folder(
                env_var="SOLVER_GLPK_PATH",
                binary_name="glpsol",
                bundled_path=tmp_path / "bundled" / "GLPK"
            )

            assert result == bundled_dir

    def test_resolve_no_solver_found_raises_error(self, tmp_path, monkeypatch):
        """Should raise RuntimeError if no solver found anywhere."""
        monkeypatch.delenv("SOLVER_GLPK_PATH", raising=False)

        with patch('shutil.which', return_value=None):
            with pytest.raises(RuntimeError) as exc_info:
                Osemosys._resolve_solver_folder(
                    env_var="SOLVER_GLPK_PATH",
                    binary_name="glpsol",
                    bundled_path=tmp_path / "nonexistent_bundled"
                )

            error_msg = str(exc_info.value)
            assert "glpsol" in error_msg
            assert "SOLVER_GLPK_PATH" in error_msg
            assert "could not be found" in error_msg.lower()


class TestOsemosysGlpkFolderProperty:
    """Test the glpkFolder property."""

    def test_glpk_folder_caching(self, tmp_path, monkeypatch):
        """Should cache the resolved folder."""
        solver_dir = tmp_path / "glpk_bin"
        solver_dir.mkdir()
        solver_binary = solver_dir / "glpsol"
        solver_binary.touch()

        monkeypatch.setenv("SOLVER_GLPK_PATH", str(solver_dir))

        # Create a mock Osemosys instance without full initialization
        osemosys = object.__new__(Osemosys)
        osemosys._glpkFolder = None
        osemosys._cbcFolder = None

        # First access
        folder1 = osemosys.glpkFolder
        # Second access (should use cached value)
        folder2 = osemosys.glpkFolder

        assert folder1 == folder2 == solver_dir


class TestOsemosysCbcFolderProperty:
    """Test the cbcFolder property."""

    def test_cbc_folder_resolution(self, tmp_path, monkeypatch):
        """Should resolve CBC solver folder."""
        solver_dir = tmp_path / "cbc_bin"
        solver_dir.mkdir()
        solver_binary = solver_dir / "cbc"
        solver_binary.touch()

        monkeypatch.setenv("SOLVER_CBC_PATH", str(solver_dir))

        # Create a mock Osemosys instance without full initialization
        osemosys = object.__new__(Osemosys)
        osemosys._glpkFolder = None
        osemosys._cbcFolder = None

        folder = osemosys.cbcFolder

        assert folder == solver_dir


class TestCrossPlatformBehavior:
    """Test cross-platform solver discovery behavior."""

    @pytest.mark.skipif(platform.system() == "Windows", reason="Unix-specific test")
    def test_unix_solver_discovery(self):
        """Test that solver discovery works on Unix systems."""
        # Check if glpsol is available on PATH
        glpsol_path = shutil.which("glpsol")
        if glpsol_path:
            # If glpsol is installed, verify we can find it
            result = Osemosys._solver_binary_names("glpsol")
            assert result == ["glpsol"]
        else:
            pytest.skip("glpsol not installed on this system")

    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows-specific test")
    def test_windows_solver_discovery(self):
        """Test that solver discovery works on Windows."""
        # Check if glpsol.exe is available on PATH
        glpsol_path = shutil.which("glpsol")
        if glpsol_path:
            # Verify .exe handling
            result = Osemosys._solver_binary_names("glpsol")
            assert "glpsol.exe" in result
        else:
            pytest.skip("glpsol not installed on this system")


class TestIntegration:
    """Integration tests for solver discovery in real scenarios."""

    def test_solver_discovery_priority_order(self, tmp_path, monkeypatch):
        """Test that env var takes priority over PATH."""
        # Create two different solver locations
        env_solver_dir = tmp_path / "env_solver"
        env_solver_dir.mkdir()
        (env_solver_dir / "glpsol").touch()

        path_solver_dir = tmp_path / "path_solver"
        path_solver_dir.mkdir()
        (path_solver_dir / "glpsol").touch()

        # Set env var to point to first location
        monkeypatch.setenv("SOLVER_GLPK_PATH", str(env_solver_dir))

        # Mock shutil.which to return second location
        with patch('shutil.which', return_value=str(path_solver_dir / "glpsol")):
            result = Osemosys._resolve_solver_folder(
                env_var="SOLVER_GLPK_PATH",
                binary_name="glpsol",
                bundled_path=tmp_path / "bundled"
            )

            # Should use env var location, not PATH
            assert result == env_solver_dir

    def test_error_message_quality(self, tmp_path, monkeypatch):
        """Test that error messages are helpful."""
        monkeypatch.delenv("SOLVER_GLPK_PATH", raising=False)

        with patch('shutil.which', return_value=None):
            with pytest.raises(RuntimeError) as exc_info:
                Osemosys._resolve_solver_folder(
                    env_var="SOLVER_GLPK_PATH",
                    binary_name="glpsol",
                    bundled_path=tmp_path / "nonexistent"
                )

            error_msg = str(exc_info.value)
            # Error should mention all three resolution methods
            assert "SOLVER_GLPK_PATH" in error_msg
            assert "PATH" in error_msg or "path" in error_msg.lower()
            assert str(tmp_path / "nonexistent") in error_msg
