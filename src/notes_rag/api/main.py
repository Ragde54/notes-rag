from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from notes_rag.api.routes import health, query
from notes_rag.db.connection import close_pool, get_pool


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await get_pool()  # warm the connection pool on startup
    yield
    await close_pool()


app = FastAPI(title="Notes RAG", lifespan=lifespan)
app.include_router(health.router)
app.include_router(query.router)
