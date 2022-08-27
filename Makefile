run:
	make test

test:
	pytest tests/

predict:
	python refactor_rossmann/predict.py --store $(STORE)

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

firefly:
	firefly predict.predict

firefly-shutdown:
	fuser -k 8000/tcp

testing:
	echo $(ARGS)