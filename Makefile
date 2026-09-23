.PHONY: rn freeze

run:
	python -m grout.main

freeze:
	pip freeze > requirements.txt
