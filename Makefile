.DEFAULT_GOAL := help
.PHONY: help clean install install-dev install-build reformat lint test dist

help: ## Print the help documentation
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean:
	rm -rf ./dist

# Check whether executed by GitHub Actions or locally
ifeq ($(GITHUB_ACTIONS), true)
    # --skip-lock installs from Pipfile so environment markers (e.g. exceptiongroup
    # for python < 3.11) are resolved against the active interpreter. A lock file
    # generated with a different Python version would otherwise omit those packages.
    INSTALL_CMD = pipenv install --skip-lock --python=$(shell which python3)
else
    # Commands for your local machine
    INSTALL_CMD = pipenv install
endif

install: ## Install runtime dependencies
	pip install pipenv
	$(INSTALL_CMD)

install-dev: install ## Install development dependencies
	$(INSTALL_CMD) --dev

install-build: ## Install build dependencies
	pip install pipenv
	$(INSTALL_CMD) --categories="build"

uninstall: ## Uninstall runtime dependencies
	pipenv uninstall --all

uninstall-dev: ## Uninstall development dependencies
	pipenv uninstall --all-dev

lint: ## Check compliance with the style guide
	pipenv run flake8 ./easyrsapy ./tests	

format: ## Format source and test code using black
	pipenv run black --skip-string-normalization ./easyrsapy
	pipenv run black --skip-string-normalization ./tests

test: lint ## Run unit tests
	pipenv run pytest -vv -s

dist: clean ## Creates a source distribution and wheel distribution
	pipenv run python -m build
	pipenv run twine check ./dist/*

tag: ## Tag version
	$(eval version := $(shell head -n 1 easyrsapy/__init__.py | sed -e "s/__version__ = //" | sed -e "s/\"//g"))
	git tag -a v$(version) -m "Bump version $(version)"
	git push origin main --follow-tags
