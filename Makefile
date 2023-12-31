ifneq (,$(wildcard ./.env))
	include .env
	export
endif

POETRY = poetry run
PYTHON = $(POETRY) python
UVICORN = $(POETRY) uvicorn --reload --port 9000

ROOT_DIR := $(shell pwd)
BACKEND_DIR := $(ROOT_DIR)/backend
FRONTEND_DIR := $(ROOT_DIR)/frontend/web_app

.PHONY: frontend backend all

install:
	cd $(BACKEND_DIR) && poetry install

backend: install
	cd $(BACKEND_DIR) && $(UVICORN) math_copilot.app:app

frontend: install
	cd $(BACKEND_DIR) && $(POETRY) python -m http.server -d $(FRONTEND_DIR)

all: install backend frontend

format: install
	cd $(BACKEND_DIR)  \
	&& $(POETRY) black . --line-length 90  \
	&& $(POETRY) isort --profile black .

test: install
	cd $(BACKEND_DIR) && $(POETRY) python -m pytest -rA tests 
