.PHONY: install run docker-up clean help

help:
	@echo "Available commands:"
	@echo "  make install    - Create virtual environment and install dependencies"
	@echo "  make run        - Run the FastAPI server locally"
	@echo "  make docker-up  - Build and run with Docker Compose"
	@echo "  make clean      - Remove venv and pycache"

install:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	@echo "Starting server..."
	. .venv/bin/activate && export PYTHONPATH=$$PYTHONPATH:$$(pwd)/src && python -m deepagent.main

docker-up:
	docker-compose up --build

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
