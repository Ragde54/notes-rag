import asyncpg

from notes_rag.config import settings
from notes_rag.ingest.embedder import get_model
from notes_rag.models import Chunk, SearchResult


async def retrieve(
    question: str, pool: asyncpg.Pool, strategy: str = "recursive"
) -> list[SearchResult]:
    model = get_model()
    q_vec = model.encode(question).tolist()

    rows = await pool.fetch(
        """
        SELECT source, chunk_index, content, strategy,
               1 - (embedding <=> $1::vector) AS score
        FROM chunks
        WHERE strategy = $2
        ORDER BY embedding <=> $1::vector
        LIMIT $3
    """,
        q_vec,
        strategy,
        settings.TOP_K,
    )

    return [
        SearchResult(
            chunk=Chunk(
                source=r["source"],
                chunk_index=r["chunk_index"],
                content=r["content"],
                strategy=r["strategy"],
            ),
            score=r["score"],
        )
        for r in rows
    ]
