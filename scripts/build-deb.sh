#!/usr/bin/env bash
set -euo pipefail

# Debian tooling reads the debian directory in place, so build from the checkout.
# Finished packages are moved afterward to keep generated output predictable.
project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
package_revision=${PACKAGE_REVISION:-1}
build_root="$project_root/build/deb"
cd "$project_root"

python3 scripts/package_metadata.py --debian-changelog debian/changelog \
    --revision "$package_revision"
dpkg-buildpackage -us -uc -b

package_name=$(dpkg-parsechangelog --show-field Source)
package_version=$(dpkg-parsechangelog --show-field Version)
mkdir -p "$build_root"
shopt -s nullglob
packages=("$project_root"/../"${package_name}_${package_version}"_*.deb)
if (( ${#packages[@]} == 0 )); then
    echo "No Debian packages were produced for ${package_name} ${package_version}." >&2
    exit 1
fi
mv -- "${packages[@]}" "$build_root/"
