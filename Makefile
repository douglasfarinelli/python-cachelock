.PHONY: help

export PYTHONPATH=$(shell pwd)/
export PYTHONDONTWRITEBYTECODE=1

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf .cache/
	@rm -rf .mypy_cache/
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

dependencies:
	@pip install pipenv
	@pipenv lock
	@pipenv install . --dev

check-types:  ## Check type annotations
	@pipenv run mypy cachelock.py --ignore-missing-imports --follow-imports=skip

flake:
	@pipenv run flake8 --max-line-length=79 cachelock.py

isort:  ## Check imports
	@pipenv run isort --recursive --diff --check-only cachelock.py tests

fix-imports:  ## Fix imports
	@pipenv run isort --recursive cachelock.py tests

lint: check-types flake isort  ## Run code lint

cov-tests: clean  ## Run coverage tests
	@pipenv run py.test --cov cachelock --cov-report=term-missing --cov-report=html:htmlcov

tests: clean  ## Run tests
	@pipenv run py.test -vv tests/

release-draft: ## Show new release changelog
	@pipenv run towncrier --draft

release-patch: ## Create patch release
	@pipenv run bumpversion patch
	@pipenv run towncrier --yes
	@git commit -am 'Update CHANGELOG' && git push && git push --tags

release-minor: ## Create minor release
	@pipenv run bumpversion minor
	@pipenv run towncrier --yes
	@git commit -am 'Update CHANGELOG' && git push && git push --tags

release-major: ## Create minor release
	@pipenv run bumpversion major
	@pipenv run towncrier --yes
	@git commit -am 'Update CHANGELOG' && git push && git push --tags

publish:  ## Publish on pypi
	@pipenv run python setup.py sdist bdist_wheel upload
	@rm -fr build dist .egg requests.egg-info
