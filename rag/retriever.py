from datetime import datetime


def temporal_rerank(results):
    """Rerank results by proximity to current year, handling missing metadata."""
    current_year = datetime.now().year
    return sorted(
        results,
        key=lambda x: abs(current_year - x.metadata.get("year", current_year))
    )


def retrieve_history(vectorstore, query):
    """Retrieve and rerank relevant market history for a query."""
    results = vectorstore.similarity_search(query, k=3)
    reranked = temporal_rerank(results)
    return "\n".join([r.page_content for r in reranked])