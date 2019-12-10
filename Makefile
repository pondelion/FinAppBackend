SHELL := /bin/bash

all: mkdoc format test typing

mkdoc:
	pipenv run pdoc --html fin_app --html-dir docs/html --overwrite

format:
	pipenv run isort -rc --atomic fin_app tests

test:
	export PYTHONPATH=./fin_app
	pipenv run pytest tests

typing:
	pipenv run mypy fin_app
