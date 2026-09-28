VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: run freeze install dev

run:
	python -m grout.main

dev:
	watchexec -e py,qml,json -r -- $(PYTHON) -m grout.main

freeze:
	pip freeze > requirements.txt

$(VENV)/bin/activate:
	python -m virtualenv $(VENV)
