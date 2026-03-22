import asyncpg
from pgvector.asyncpg import register_vector

from notes_rag.config import settings

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.DATABASE_URL)
        async with _pool.acquire() as conn:
            await register_vector(conn)
    return _pool


async def close_pool() -> None:
    if _pool:
        await _pool.close()
