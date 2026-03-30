import importlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_DIR = PROJECT_ROOT / "API"


class AppSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(API_DIR))
        os.environ.setdefault("MUIOGO_SECRET_KEY", "smoke-test-secret")
        cls.app_module = importlib.import_module("app")
        cls.client = cls.app_module.app.test_client()

    def test_app_import_from_arbitrary_cwd(self):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(API_DIR)
        env.setdefault("MUIOGO_SECRET_KEY", "smoke-test-secret")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                [sys.executable, "-c", "import app; print(app.app.import_name)"],
                cwd=tmpdir,
                env=env,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("app", result.stdout.strip())

    def test_home_route(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<!DOCTYPE html>", response.data)

    def test_get_session_route(self):
        response = self.client.get("/getSession")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"session": None})

    def test_clear_session_route(self):
        response = self.client.post("/setSession", json={"case": None})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"osycase": None})

    def test_repo_has_no_unmerged_paths(self):
        result = subprocess.run(
            ["git", "ls-files", "-u"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
