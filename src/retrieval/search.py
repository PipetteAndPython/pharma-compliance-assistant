# =========================
# RETRIEVAL (FAISS SEARCH)
# =========================

import numpy as np
from src.processing.embeddings import create_query_embeddings


def search(query, index, chunks, k=5):
    """
    Converts query into embedding and searches for relevant chunks in FAISS.
    """

    query_vector = np.array(create_query_embeddings(query), dtype=np.float32)

    if query_vector is None or len(query_vector) == 0:
        return []

    query_vector = query_vector.reshape(1, -1)

    distances, indices = index.search(query_vector, k)

    if indices is None or len(indices) == 0 or len(indices[0]) == 0:
        return []

    results = []

    for i, score in zip(indices[0], distances[0]):

        # FAISS returns -1 when there are not enough neighbors
        if i == -1:
            continue

        # Safety check against invalid indices
        if i < 0 or i >= len(chunks):
            continue

        chunk = chunks[i]

        results.append({
            "file": chunk.get("file", "unknown"),
            "text": chunk.get("text", ""),
            "score": float(score)
        })

    return results