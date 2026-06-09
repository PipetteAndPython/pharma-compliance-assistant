
from sentence_transformers import SentenceTransformer

# Modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(all_chunks):

    # Extrae el texto de cada chunk
    texts = [chunk["text"] for chunk in all_chunks]

    # Genera embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings

def create_query_embeddings(text):
    return create_embeddings([text])