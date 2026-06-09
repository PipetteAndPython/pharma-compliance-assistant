# =========================
# FAISS VECTOR STORE
# =========================
# Build, save, and load FAISS indexes for semantic search

import faiss
import numpy as np


# =========================
# BUILD INDEX
# =========================

def build_faiss_index(embeddings):
    """
    Builds a FAISS index from a numpy array of embeddings.
    Uses L2 (Euclidean) distance for similarity search.
    """

    if embeddings is None or len(embeddings) == 0:
        raise ValueError("❌ Cannot build FAISS index: embeddings array is empty.")

    vectors = np.array(embeddings).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    return index


# =========================
# SAVE INDEX
# =========================

def save_index(index, path):
    """
    Saves a FAISS index to disk.
    """

    faiss.write_index(index, str(path))


# =========================
# LOAD INDEX
# =========================

def load_index(path):
    """
    Loads a FAISS index from disk.
    Returns None if the file cannot be read.
    """

    try:
        return faiss.read_index(str(path))
    except Exception as e:
        print(f"❌ Error loading FAISS index: {e}")
        return None