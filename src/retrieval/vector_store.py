import faiss
# Librería para búsqueda rápida de vectores

import numpy as np
# FAISS trabaja mejor con arrays de numpy


def build_faiss_index(embeddings):

    # Obtiene cuántos números tiene cada embedding
    # Ejemplo: 384 dimensiones
    dimension = embeddings.shape[1]

    # Creamos un índice FAISS usando distancia euclidiana (L2)
    index = faiss.IndexFlatL2(dimension)

    # Convertimos embeddings a float32
    # FAISS necesita este formato
    embeddings = np.array(embeddings).astype("float32")

    # Agrega todos los embeddings al índice
    index.add(embeddings)

    return index