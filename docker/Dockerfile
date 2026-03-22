FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev

COPY src/ src/
RUN uv pip install -e . --no-deps

CMD ["uvicorn", "notes_rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]