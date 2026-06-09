# =========================
# QUERY PIPELINE (RAG - SEARCH)
# =========================
# Development and debugging tool only.
# This script queries the FAISS index directly and returns raw chunks,
# WITHOUT passing them through the LLM.
#
# Use this to verify that semantic search is working correctly
# before involving the language model.
#
# For the full RAG experience (search + LLM response), use:
#   → app/rag_assistant.py
#
# Flow: question → embedding → FAISS → relevant chunks → output

from pathlib import Path
import sys
import json

# =========================
# PROJECT CONFIGURATION
# =========================
# Ensures Python can import modules from src/

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# =========================
# SYSTEM IMPORTS
# =========================

from src.vectorstore.faiss_store import load_index
from src.retrieval.search import search

# =========================
# FILE PATHS
# =========================

INDEX_PATH = PROJECT_ROOT / "data" / "vector_store" / "index.faiss"
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks" / "chunks.json"

# =========================
# LOAD PERSISTED DATA
# =========================

print("📦 Loading FAISS index and chunks...")

# Load FAISS index
index = load_index(INDEX_PATH)
if index is None:
    raise ValueError("FAISS index could not be loaded correctly")

# Load chunks (metadata associated with embeddings)
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks_list = json.load(f)

# Convert to index-based access
chunks = {i: chunk for i, chunk in enumerate(chunks_list)}

print("✔ System ready for queries")


# =========================
# USER INTERFACE (CLI)
# =========================

if __name__ == "__main__":

    print("\n🧠 RAG Query System ready (debug mode)")
    print("Type your question (or 'exit' to quit)\n")

    while True:

        # User input
        question = input("Question: ")

        if question.lower() == "exit":
            print("👋 Exiting system")
            break

        # Semantic search
        results = search(question, index, chunks)

        if not results:
            print("⚠️ No results found.\n")
            continue

        # =========================
        # CONTEXT OUTPUT
        # =========================
        print("\n📄 Results:\n")

        for r in results:
            print("📌 File:", r["file"])
            print("⭐ Score:", round(r["score"], 4))
            print(r["text"][:300])
            print("-" * 50)
