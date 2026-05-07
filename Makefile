.PHONY: install install-dev install-all test lint typecheck check build clean docker-build docker-run

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-all:
	pip install -e ".[dev,build]"

test:
	python -m pytest --cov --cov-report=term-missing

lint:
	ruff check src/gmail_creator/ tests/

typecheck:
	mypy src/gmail_creator/ --explicit-package-bases

check: lint typecheck test

build:
	pyinstaller gmail_creator.spec

clean:
	rm -rf build/ dist/ *.spec
	rm -rf .pytest_cache .ruff_cache __pycache__
	rm -rf src/gmail_creator/__pycache__
	rm -rf src/gmail_creator/*.egg-info
	rm -rf tests/__pycache__

docker-build:
	docker build -t gmail-creator-pro .

docker-run:
	docker run -it --rm \
		-e GMAIL_HEADLESS=1 \
		-v "$(PWD)/config:/app/config" \
		-v "$(PWD)/data:/app/data" \
		gmail-creator-pro
