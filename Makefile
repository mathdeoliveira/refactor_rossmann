run:
	make test

test:
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y .
