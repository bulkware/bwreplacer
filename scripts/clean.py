#!/usr/bin/env python3
"""Remove build output and Python caches without touching project data."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
ROOT_OUTPUTS = (
    "build", "dist", ".eggs", "htmlcov", ".pytest_cache", ".coverage",
)


def cleanup_paths(root: Path) -> list[Path]:
    """Find disposable outputs without following symlinks outside the checkout."""
    candidates = {root / name for name in ROOT_OUTPUTS}
    candidates.update(root.glob("*.egg-info"))
    for name in ("tests", "scripts"):
        tree = root / name
        if tree.is_symlink() or not tree.exists():
            continue
        for directory, subdirectories, _ in os.walk(tree, followlinks=False):
            base = Path(directory)
            if "__pycache__" in subdirectories:
                candidates.add(base / "__pycache__")
                subdirectories.remove("__pycache__")
    for cache in root.glob("__pycache__"):
        candidates.add(cache)
    return sorted(path for path in candidates if path.exists() or path.is_symlink())


def main() -> int:
    """Preview or remove known generated directories and files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="only list paths to remove")
    arguments = parser.parse_args()
    # Restrict cleanup to disposable paths rooted in this checkout.
    for target in cleanup_paths(ROOT):
        print(f"{'Would remove' if arguments.dry_run else 'Removing'} {target.relative_to(ROOT)}")
        if arguments.dry_run:
            continue
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
