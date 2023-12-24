export PIPELINE_NAME = fifa-predictior-pipeline
export IMAGE_NAME = localhost:5000/$(PIPELINE_NAME):$(TAG)
export KF_PIPELINES_ENDPOINT = http://192.168.0.150.nip.io/
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

clean:
	rm -rf models/*
	rm -f *.yaml

create-model: clean
	python src/train.py

kfp-compile: clean
	python pipelines/dsl.py

build:
	docker build -t $(IMAGE_NAME) .

push:
	docker push $(IMAGE_NAME)

deploy:
	kfp pipeline --endpoint $(KF_PIPELINES_ENDPOINT) create -p $(PIPELINE_NAME) $(PIPELINE_NAME).yaml


call-model:
	TOKEN=$(kubectl create token default-editor -n kubeflow-user-example-com --audience=istio-ingressgateway.istio-system.svc.cluster.local --duration=24h)
	curl -v -H "Host: fifa-predictior-predictor.kubeflow-user-example-com.example.com" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" http://localhost:8080/v1/models/fifa-predictior:predict -d @example-input/input.json