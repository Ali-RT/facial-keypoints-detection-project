.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 lint/black
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint/flake8: ## check style with flake8
	flake8 facial_keypoints_detection tests
lint/black: ## check style with black
	black --check facial_keypoints_detection tests

lint: lint/flake8 lint/black ## check style

test: ## run tests quickly with the default Python
	python setup.py test

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source facial_keypoints_detection setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/facial_keypoints_detection.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ facial_keypoints_detection
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install


# MAKE               := make --no-print-directory

# DESCRIBE           := $(shell git describe --match "v*" --always --tags)
# DESCRIBE_PARTS     := $(subst -, ,$(DESCRIBE))

# VERSION_TAG        := $(word 1,$(DESCRIBE_PARTS))
# COMMITS_SINCE_TAG  := $(word 2,$(DESCRIBE_PARTS))

# VERSION            := $(subst v,,$(VERSION_TAG))
# VERSION_PARTS      := $(subst ., ,$(VERSION))

# MAJOR              := $(word 1,$(VERSION_PARTS))
# MINOR              := $(word 2,$(VERSION_PARTS))
# MICRO              := $(word 3,$(VERSION_PARTS))

# NEXT_MAJOR         := $(shell echo $$(($(MAJOR)+1)))
# NEXT_MINOR         := $(shell echo $$(($(MINOR)+1)))
# NEXT_MICRO          = $(shell echo $$(($(MICRO)+$(COMMITS_SINCE_TAG))))

# ifeq ($(strip $(COMMITS_SINCE_TAG)),)
# CURRENT_VERSION_MICRO := $(MAJOR).$(MINOR).$(MICRO)
# CURRENT_VERSION_MINOR := $(CURRENT_VERSION_MICRO)
# CURRENT_VERSION_MAJOR := $(CURRENT_VERSION_MICRO)
# else
# CURRENT_VERSION_MICRO := $(MAJOR).$(MINOR).$(NEXT_MICRO)
# CURRENT_VERSION_MINOR := $(MAJOR).$(NEXT_MINOR).0
# CURRENT_VERSION_MAJOR := $(NEXT_MAJOR).0.0
# endif

# DATE                = $(shell date +'%d.%m.%Y')
# TIME                = $(shell date +'%H:%M:%S')
# COMMIT             := $(shell git rev-parse HEAD)
# AUTHOR             := $(firstword $(subst @, ,$(shell git show --format="%aE" $(COMMIT))))
# BRANCH_NAME        := $(shell git rev-parse --abbrev-ref HEAD)

# TAG_MESSAGE         = "$(TIME) $(DATE) $(AUTHOR) $(BRANCH_NAME)"
# COMMIT_MESSAGE     := $(shell git log --format=%B -n 1 $(COMMIT))

# CURRENT_TAG_MICRO  := "v$(CURRENT_VERSION_MICRO)"
# CURRENT_TAG_MINOR  := "v$(CURRENT_VERSION_MINOR)"
# CURRENT_TAG_MAJOR  := "v$(CURRENT_VERSION_MAJOR)"

# # --- Version commands ---

# .PHONY: version
# version:
# 	@$(MAKE) version-micro

# .PHONY: version-micro
# version-micro:
# 	@echo "$(CURRENT_VERSION_MICRO)"

# .PHONY: version-minor
# version-minor:
# 	@echo "$(CURRENT_VERSION_MINOR)"

# .PHONY: version-major
# version-major:
# 	@echo "$(CURRENT_VERSION_MAJOR)"

# # --- Tag commands ---

# .PHONY: tag-micro
# tag-micro:
# 	@echo "$(CURRENT_TAG_MICRO)"

# .PHONY: tag-minor
# tag-minor:
# 	@echo "$(CURRENT_TAG_MINOR)"

# .PHONY: tag-major
# tag-major:
# 	@echo "$(CURRENT_TAG_MAJOR)"

# # -- Meta info ---

# .PHONY: tag-message
# tag-message:
# 	@echo "$(TAG_MESSAGE)"

# .PHONY: commit-message
# commit-message:
# 	@echo "$(COMMIT_MESSAGE)"

# Semantic versioning details: https://semver.org/
# Constants

# VERSION_FILE=setup.py
# help:                      ## Show this help.
# 	@grep -h "##" $(MAKEFILE_LIST) | grep -v grep | tr -d '##' | tr -d '$$'

# release-patch:             ## Tag the release as a patch release and push tag to git.
# 	./sem_ver.sh $(VERSION_FILE) release-patch

# release-minor:             ## Tag the release as a minor  releaseand push tag to git.
# 	./sem_ver.sh $(VERSION_FILE) release-minor

# release-major:             ## Tag the release as a major release and push tag to git.
# 	./sem_ver.sh $(VERSION_FILE) release-major


# Semantic Versioning
VERSION=$(shell python -c "from setuptools_scm import get_version; print(get_version())")

.PHONY: version
version:
	@echo $(VERSION)

.PHONY: bump-major bump-minor bump-patch
bump-major bump-minor bump-patch:
	bumpversion $(@:bump-%=%)
