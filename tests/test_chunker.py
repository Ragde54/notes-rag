from notes_rag.ingest.chunker import chunk_recursive, chunk_semantic

SAMPLE = """# Intro\n\nThis is a test note. It has multiple sentences. \
    Sentence three here.\n\n## Section Two\n\nAnother paragraph with more content."""


def test_recursive_produces_chunks() -> None:
    chunks = chunk_recursive("test.md", SAMPLE)
    assert len(chunks) > 0
    assert all(c.strategy == "recursive" for c in chunks)


def test_semantic_produces_chunks() -> None:
    chunks = chunk_semantic("test.md", SAMPLE)
    assert len(chunks) > 0


def test_chunk_index_is_sequential() -> None:
    chunks = chunk_recursive("test.md", SAMPLE)
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))
