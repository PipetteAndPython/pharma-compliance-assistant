# =========================
# TEXT SPLITTER
# =========================
# Splits long text into overlapping chunks

def chunk_text(text, chunk_size=1000, overlap=200, min_chunk_size=100):
    """
    Splits a text into chunks with overlap to preserve context.

    Args:
        text: full text to split
        chunk_size: maximum size of each chunk (in characters)
        overlap: overlap between chunks to avoid losing context
        min_chunk_size: minimum size to consider a chunk valid
    """

    if not text or not text.strip():
        return []

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size

        # If not the last chunk, try to cut at a space
        # to avoid splitting words in the middle
        if end < len(text):
            space_index = text.rfind(" ", start, end)
            if space_index != -1:
                end = space_index

        chunk = text[start:end].strip()

        # Only keep chunks with enough content
        if len(chunk) >= min_chunk_size:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks