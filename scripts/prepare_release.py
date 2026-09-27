#!/usr/bin/env python3
"""Synchronize release metadata with the latest published changelog entry."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from package_metadata import parse_changelog


def sync_pyproject(path: Path, version: str) -> str:
    """Update the PEP 621 project version without changing other TOML sections."""
    contents = path.read_text(encoding="utf-8")
    project = re.search(r"^\[project\]$", contents, re.MULTILINE)
    if project is None:
        raise ValueError("pyproject.toml has no [project] section")
    version_line = re.compile(r"^version = \"[^\"]+\"$", re.MULTILINE)
    match = version_line.search(contents, project.end())
    if match is None:
        raise ValueError("pyproject.toml has no project version")
    return f"{contents[:match.start()]}version = \"{version}\"{contents[match.end():]}"


def sync_appstream(path: Path, version: str, release_date: str) -> str:
    """Prepend one public release to AppStream metadata, retaining prior releases."""
    contents = path.read_text(encoding="utf-8")
    existing = re.search(rf'<release version="{re.escape(version)}" date="(?P<date>[^"]+)"/>',
                         contents)
    if existing:
        if existing["date"] != release_date:
            raise ValueError(f"AppStream metadata has a different date for release {version}")
        return contents
    marker = "  <releases>\n"
    if marker not in contents:
        raise ValueError("AppStream metadata has no releases section")
    release = f'    <release version="{version}" date="{release_date}"/>\n'
    return contents.replace(marker, marker + release, 1)


def sync_release(root: Path) -> None:
    """Read the latest changelog release, then update derived release metadata."""
    changelog = root / "CHANGELOG.md"
    release = parse_changelog(changelog)
    pyproject = root / "pyproject.toml"
    appstream = root / "data/org.bulkware.bwreplacer.metainfo.xml"
    release_date = release.release_date.isoformat()
    updates = {
        pyproject: sync_pyproject(pyproject, release.version),
        appstream: sync_appstream(appstream, release.version, release_date),
    }
    for path, contents in updates.items():
        path.write_text(contents, encoding="utf-8")


def main() -> int:
    """Synchronize release metadata from the changelog in this checkout."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        sync_release(Path(__file__).resolve().parents[1])
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
