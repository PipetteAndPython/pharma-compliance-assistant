# =========================
# EMBEDDINGS
# =========================
# Loads the sentence transformer model and generates embeddings
# for both chunks and queries

from sentence_transformers import SentenceTransformer
import numpy as np

# Load model once to avoid reloading on every call
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# CHUNK EMBEDDINGS
# =========================

def create_embeddings(all_chunks):
    """
    Generates embeddings for a list of chunks.
    Returns a numpy array of float32 vectors.
    """

    if not all_chunks:
        return np.array([])

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings.astype("float32")

# =========================
# QUERY EMBEDDING
# =========================

def create_query_embeddings(text):
    """
    Generates an embedding for a single query string.
    Returns a numpy array of float32.
    """

    if not text or not text.strip():
        return np.array([])

    embedding = model.encode(
        [text],
        convert_to_numpy=True
    )

    return embedding.astype("float32")