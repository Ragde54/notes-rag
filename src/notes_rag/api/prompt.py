from notes_rag.models import SearchResult


def build_prompt(question: str, results: list[SearchResult]) -> str:
    """
    Constructs a RAG prompt using the provided question and search results.
    """
    context_parts = []
    for r in results:
        part = f"Source: {r.chunk.source}\nContent: {r.chunk.content}"
        context_parts.append(part)

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""Use the following context to answer the user's question. 
If the answer is not in the context, say you don't know and don't make things up.

Context:
{context}

Question: {question}

Answer:"""
    return prompt
