from sentence_transformers import SentenceTransformer

from notes_rag.config import settings
from notes_rag.models import Chunk

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_chunks(chunks: list[Chunk]) -> list[Chunk]:
    model = get_model()
    texts = [c.content for c in chunks]
    vectors = model.encode(texts, batch_size=32, show_progress_bar=True)
    for chunk, vec in zip(chunks, vectors):
        chunk.embedding = vec.tolist()
    return chunks
