SHELL := /bin/bash

export PYTHONPATH := .:$(PYTHONPATH)
export MYPYPATH := ./fin_app:$(MYPYPATH)

all: mkdoc format test typing 

mkdoc:
	pipenv run pdoc --html fin_app --html-dir docs/html --overwrite

format:
	pipenv run isort -rc --atomic fin_app tests

typing:
	pipenv run mypy fin_app/**/*.py 
	pipenv run mypy fin_app/**/**/*.py

test:
	pipenv run pytest tests
