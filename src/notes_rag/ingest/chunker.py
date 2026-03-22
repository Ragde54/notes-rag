import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from notes_rag.config import settings
from notes_rag.models import Chunk


def chunk_recursive(source: str, text: str) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""],
    )
    pieces = splitter.split_text(text)
    return [
        Chunk(source=source, chunk_index=i, content=p, strategy="recursive")
        for i, p in enumerate(pieces)
    ]


def chunk_semantic(source: str, text: str) -> list[Chunk]:
    # Group sentences into windows of ~N sentences, sliding by 1
    raw_sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    # Ensure we only have non-empty strings and satisfy strict type checkers
    sentences = [s for s in raw_sentences if s]

    window = 5
    stride = 2
    groups: list[str] = []

    num_sentences = len(sentences)
    for i in range(0, max(1, num_sentences - window + 1), stride):
        # Explicit slicing with a middle variable
        end_idx = i + window
        segment = sentences[i:end_idx]
        if segment:
            groups.append(" ".join(segment))

    return [
        Chunk(source=source, chunk_index=idx, content=g, strategy="semantic")
        for idx, g in enumerate(groups)
    ]
