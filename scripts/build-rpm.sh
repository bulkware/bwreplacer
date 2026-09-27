#!/usr/bin/env bash
set -euo pipefail

# Stage only release inputs so RPM never receives local caches or settings.
project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
package_revision=${PACKAGE_REVISION:-1}
build_root="$project_root/build/rpm/rpmbuild"
staging_root=$(mktemp -d)
trap 'rm -rf "$staging_root"' EXIT

cd "$project_root"
version=$(python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')
rm -rf "$build_root"
mkdir -p "$build_root"/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

source_root="$staging_root/bwreplacer-$version"
mkdir -p "$source_root"
cp pyproject.toml README.md CHANGELOG.md MANIFEST.in license.txt gpl.txt icons.txt "$source_root/"
cp *.py *.ui *.png *.ico *.db "$source_root/"
cp -R assets data docs tests scripts packaging debian "$source_root/"
tar -czf "$build_root/SOURCES/bwreplacer-$version.tar.gz" -C "$staging_root" "bwreplacer-$version"

spec_stage="$staging_root/bwreplacer.spec"
cp packaging/rpm/bwreplacer.spec "$spec_stage"
python3 scripts/package_metadata.py --rpm-spec "$spec_stage" --revision "$package_revision"
rpmbuild --define "_topdir $build_root" -ba "$spec_stage"
