from typing import Annotated, Any

import asyncpg
import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from notes_rag.api.prompt import build_prompt
from notes_rag.api.retriever import retrieve
from notes_rag.config import settings
from notes_rag.db.connection import get_pool

router = APIRouter()


class AskRequest(BaseModel):
    question: str
    strategy: str = "recursive"


class AskResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]
    strategy: str


async def get_pool_dep() -> asyncpg.Pool:
    return await get_pool()


PoolDep = Annotated[asyncpg.Pool, Depends(get_pool_dep)]


@router.post("/ask", response_model=AskResponse)  # type: ignore[untyped-decorator]
async def ask(req: AskRequest, pool: PoolDep) -> AskResponse:
    results = await retrieve(req.question, pool, req.strategy)
    prompt = build_prompt(req.question, results)

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
        )
        answer = resp.json()["response"]

    return AskResponse(
        answer=answer,
        sources=[{"source": r.chunk.source, "score": float(r.score)} for r in results],
        strategy=req.strategy,
    )
