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
	rm -rf models/*.pkl
	python src/train.py