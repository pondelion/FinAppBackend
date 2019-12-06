SHELL := /bin/bash

all: mkdoc

mkdoc:
	pipenv run pdoc --html fin_app --html-dir docs --overwrite
