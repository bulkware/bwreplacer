PYTHON ?= python3
PACKAGE_REVISION ?= 1
SUDO ?= sudo
.DEFAULT_GOAL := help
.PHONY: help run test coverage lint check build prepare-release install-deb install-rpm deb rpm windows clean clean-dry-run

RUN_ARGUMENTS := $(filter-out run,$(MAKECMDGOALS))
ifneq ($(strip $(RUN_ARGUMENTS)),)
.PHONY: $(RUN_ARGUMENTS)
$(RUN_ARGUMENTS):
endif

help:
	@echo "make run [FILE]     Run bwReplacer, optionally adding files"
	@echo "make test           Run display-free unit tests"
	@echo "make coverage       Measure application-code test coverage"
	@echo "make lint           Run PyLint on maintained source files"
	@echo "make check          Run tests and lint"
	@echo "make build          Build Python source and wheel distributions"
	@echo "make prepare-release  Synchronize metadata with the latest CHANGELOG release"
	@echo "make install-deb    Install Debian Trixie package build dependencies"
	@echo "make install-rpm    Install Fedora/RHEL package build dependencies"
	@echo "make deb            Build a Debian package"
	@echo "make rpm            Build an RPM package"
	@echo "make windows        Build Windows MSI and portable ZIP (Windows only)"
	@echo "make clean          Remove generated build and cache files"
	@echo "make clean-dry-run  Preview generated files to remove"

run:
	PYTHONPATH=.. $(PYTHON) -m bwreplacer.main $(RUN_ARGUMENTS)

test:
	PYTHONPATH=.. $(PYTHON) -m unittest discover -s tests -v

coverage:
	PYTHONPATH=.. $(PYTHON) -m coverage run -m unittest discover -s tests -v
	$(PYTHON) -m coverage report -m

lint:
	PYTHONPATH=.. $(PYTHON) -m pylint --persistent=no main.py datahandler.py filehandler.py \
		stringhandler.py functions.py resources.py \
		tests scripts/clean.py scripts/package_metadata.py scripts/prepare_release.py

check: test lint

build:
	$(PYTHON) -m build

prepare-release:
	$(PYTHON) scripts/prepare_release.py

install-deb:
	$(SUDO) apt-get update
	$(SUDO) apt-get -y install appstream debhelper dh-python dpkg-dev \
		pybuild-plugin-pyproject python3-all python3-pyside6.qtwidgets python3-setuptools

install-rpm:
	$(SUDO) dnf --assumeyes install dnf-plugins-core rpm-build
	$(SUDO) dnf --assumeyes builddep packaging/rpm/bwreplacer.spec

deb:
	PACKAGE_REVISION="$(PACKAGE_REVISION)" bash scripts/build-deb.sh

rpm:
	PACKAGE_REVISION="$(PACKAGE_REVISION)" bash scripts/build-rpm.sh

windows:
	powershell.exe -ExecutionPolicy Bypass -File scripts/build-windows.ps1

clean:
	$(PYTHON) scripts/clean.py

clean-dry-run:
	$(PYTHON) scripts/clean.py --dry-run
