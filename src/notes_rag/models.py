from dataclasses import dataclass, field


@dataclass
class Chunk:
    source: str
    chunk_index: int
    content: str
    strategy: str
    embedding: list[float] | None = field(default=None, repr=False)


@dataclass
class SearchResult:
    chunk: Chunk
    score: float
