import numpy as np

from src.processing.embeddings import model
# Reutilizamos el mismo modelo de embeddings


def search(query, index, all_chunks, k=5):

    # Convierte la pregunta del usuario en embedding
    query_embedding = model.encode([query])

    # FAISS necesita float32
    query_embedding = np.array(query_embedding).astype("float32")

    # Busca los k chunks más similares
    distances, indices = index.search(query_embedding, k)

    results = []

    # Recorremos los resultados encontrados
    for i in indices[0]:

        # Guardamos el chunk correspondiente
        results.append(all_chunks[i])

    return results