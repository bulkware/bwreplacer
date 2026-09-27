Name:           bwreplacer
Version:        1.6.0
Release:        1%{?dist}
Summary:        Desktop application for correcting spelling errors in text files

License:        GPL-3.0-or-later
URL:            https://github.com/bulkware/bwreplacer
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pyside6
BuildRequires:  python3-setuptools
BuildRequires:  pyproject-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  appstream
Requires:       python3-pyside6

%description
bwReplacer applies correction lists to text files.

%prep
%autosetup

%build
%pyproject_wheel

%check
PYTHONPATH=.. %{python3} -m unittest discover -s tests -v

%install
%pyproject_install
install -D -m 644 data/org.bulkware.bwreplacer.desktop \
    %{buildroot}%{_datadir}/applications/org.bulkware.bwreplacer.desktop
install -D -m 644 data/org.bulkware.bwreplacer.metainfo.xml \
    %{buildroot}%{_metainfodir}/org.bulkware.bwreplacer.metainfo.xml
install -D -m 644 data/icons/hicolor/512x512/apps/org.bulkware.bwreplacer.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/org.bulkware.bwreplacer.png

%files
%license gpl.txt
%doc CHANGELOG.md README.md
%{_bindir}/bwreplacer
%{python3_sitelib}/bwreplacer
%{python3_sitelib}/bwreplacer-*.dist-info
%{_datadir}/applications/org.bulkware.bwreplacer.desktop
%{_metainfodir}/org.bulkware.bwreplacer.metainfo.xml
%{_datadir}/icons/hicolor/512x512/apps/org.bulkware.bwreplacer.png

%changelog
* Sun Sep 27 2026 Antti-Pekka Meronen <antice@kapsi.fi> - 1.6.0-1
- Changed: GitHub Actions CI package building.
- Changed: Packaging system for Debian (.deb) and Red Hat (.rpm) based distros.
- Changed: Renewed the Windows packaging system.
