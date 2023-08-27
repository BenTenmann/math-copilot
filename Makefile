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

backend:
	cd $(BACKEND_DIR) && $(UVICORN) math_copilot.app:app

frontend:
	cd $(BACKEND_DIR) && $(POETRY) python -m http.server -d $(FRONTEND_DIR)

all: backend frontend
