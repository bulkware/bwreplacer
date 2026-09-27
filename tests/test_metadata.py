"""Validate the release metadata consumed by package builders."""

from importlib.metadata import PackageNotFoundError
from pathlib import Path
import runpy
import tomllib
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


class MetadataTests(unittest.TestCase):
    """Keep the version authority and current changelog release synchronized."""

    def test_current_release_matches_project_metadata(self):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(f"## [{project['version']}] - 2026-09-27", changelog)

    def test_only_pyside_is_a_runtime_dependency(self):
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
        self.assertEqual(project["dependencies"], ["PySide6>=6.0"])

    def test_runtime_version_uses_distribution_metadata_with_source_fallback(self):
        with mock.patch("importlib.metadata.version", return_value="9.8.7"):
            metadata = runpy.run_path(ROOT / "__init__.py")
            self.assertEqual(metadata["__version__"], "9.8.7")
        with mock.patch("importlib.metadata.version", side_effect=PackageNotFoundError):
            metadata = runpy.run_path(ROOT / "__init__.py")
            self.assertEqual(metadata["__version__"], "development")
