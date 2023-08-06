ifneq (,$(wildcard ./.env))
	include .env
	export
endif

POETRY = poetry run
PYTHON = $(POETRY) python
UVICORN = $(POETRY) uvicorn --reload --port 9000

.PHONY: frontend backend all

backend:
	cd backend && $(UVICORN) math_copilot.app:app

frontend:
	python -m http.server -d ./frontend/web_app

all: backend frontend
