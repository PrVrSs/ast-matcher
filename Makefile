SHELL := /usr/bin/env bash

.PHONY: unit
unit:
	poetry run pytest -v \
		-vv \
		--cov=ast_matcher \
		--capture=no \
		--cov-report=term-missing \
 		--cov-config=.coveragerc \
 		--cov-report=xml \

.PHONY: mypy
mypy:
	poetry run mypy ast_matcher

.PHONY: lint
lint:
	poetry run pylint ast_matcher

test: lint mypy unit
