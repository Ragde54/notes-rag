from fastapi import APIRouter

from notes_rag.db.connection import get_pool

router = APIRouter()


@router.get("/health")  # type: ignore[untyped-decorator]
async def health() -> dict[str, str]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.fetchval("SELECT 1")
    return {"status": "ok"}
