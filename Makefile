.PHONY: up down ingest test lint fmt typecheck

up:
	docker compose up -d
	@echo "Waiting for DB..."
	@sleep 2
	$(MAKE) migrate

down:
	docker compose down

migrate:
	uv run alembic upgrade head

setup-ollama:
	docker compose exec ollama ollama pull llama3.2

ingest:
	uv run python -m notes_rag.ingest.run

test:
	uv run pytest --cov=src/notes_rag

lint:
	uv run ruff check src/ tests/

fmt:
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/