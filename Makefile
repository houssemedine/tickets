.PHONY: run test cov lint format docker-build docker-run

UV := $(shell command -v uv 2>/dev/null)
ifeq ($(UV),)
UV := $(HOME)/.local/bin/uv
endif

APP := app.main:app
IMAGE := ticket-managements:latest
CONTAINER := ticket-managements

run:
	$(UV) run uvicorn $(APP) --reload

test:
	$(UV) run pytest -q

cov:
	$(UV) run pytest --cov=app --cov-report=term-missing

lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run -d --rm --name $(CONTAINER) -p 8010:8010 $(IMAGE)
