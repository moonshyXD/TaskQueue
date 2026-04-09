.PHONY: run test build lint testcover

build:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync

run:
	python3 main.py

lint:
	ruff format .
	ruff check --fix
	mypy .

testcover:
	pytest --cov --cov-report=term-missing

test:
	pytest