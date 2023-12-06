install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

format:
	isort .
	black -l 120 src

check-format:
	isort . --check
	black -l 120 --check src

lint:
	flake8 src

create_model:
	rm -rf models/*
	python src/train.py

kfp-compile-pipeline:
	kfp dsl compile --py pipelines/dsl.py --output pipelines/$(PIPELINE_NAME).yaml

build:
	docker build -t $(IMAGE_NAME) .

push:
	docker push $(IMAGE_NAME)

deploy:
	kfp pipeline --endpoint $(ENDPOINT) create -p $(PIPELINE_NAME) pipelines/$(PIPELINE_NAME).yaml
