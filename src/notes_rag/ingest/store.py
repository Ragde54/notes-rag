import psycopg2
from psycopg2.extras import execute_values

from notes_rag.config import settings
from notes_rag.models import Chunk


def upsert_chunks(chunks: list[Chunk]) -> None:
    conn = psycopg2.connect(settings.DATABASE_URL)
    with conn, conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO chunks (source, chunk_index, content, embedding, strategy)
            VALUES %s
            ON CONFLICT (source, chunk_index, strategy)
            DO UPDATE SET content = EXCLUDED.content,
                          embedding = EXCLUDED.embedding
        """,
            [
                (
                    c.source,
                    c.chunk_index,
                    c.content,
                    f"[{','.join(map(str, c.embedding))}]" if c.embedding else None,
                    c.strategy,
                )
                for c in chunks
            ],
        )
    conn.close()
