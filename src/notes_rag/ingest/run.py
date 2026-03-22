import typer

from notes_rag.config import settings
from notes_rag.ingest.chunker import chunk_recursive, chunk_semantic
from notes_rag.ingest.embedder import embed_chunks
from notes_rag.ingest.loader import load_markdown_files
from notes_rag.ingest.store import upsert_chunks

app = typer.Typer()


@app.command()  # type: ignore[untyped-decorator]
def ingest(strategy: str = "both") -> None:
    docs = load_markdown_files(settings.NOTES_DIR)
    for source, text in docs:
        for fn, strat in [
            (chunk_recursive, "recursive"),
            (chunk_semantic, "semantic"),
        ]:
            if strategy not in ("both", strat):
                continue
            chunks = fn(source, text)
            chunks = embed_chunks(chunks)
            upsert_chunks(chunks)
            print(f"{strat}: {len(chunks)} chunks from {source}")


if __name__ == "__main__":
    app()
