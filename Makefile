SHELL := /bin/bash

all: mkdoc format

mkdoc:
	pipenv run pdoc --html fin_app --html-dir docs/html --overwrite

format:
	pipenv run isort -rc --atomic fin_app tests
