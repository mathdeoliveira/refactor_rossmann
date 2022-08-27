run:
	make test

test:
	pytest tests/

train:
	python refactor_rossmann/train.py

quality_checks:
	isort .
	black .
	pylint --recursive=y .

mlflow:
	mlflow ui --backend-store-uri sqlite:///mlflow.db

mlflow-shutdown:
	fuser -k 5000/tcp
