"""Locate bundled application assets in source, installed, and frozen builds."""

from importlib.resources import files
from pathlib import Path
import sys


def asset_path(name: str) -> str:
    """Return an absolute path to a bundled application asset."""
    if getattr(sys, "frozen", False):
        return str(Path(sys.executable).resolve().parent / "assets" / name)
    return str(files("bwreplacer").joinpath(name))
