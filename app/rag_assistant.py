# =========================
# RAG ASSISTANT (QUERY + LLM)
# =========================
# Full RAG pipeline: question → embedding → FAISS → context → LLM → answer
# This is the main entry point for the assistant.
# For debug/search-only mode, use: app/query.py

from pathlib import Path
import sys
import json

# =========================
# PROJECT CONFIGURATION
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

# =========================
# INTERNAL IMPORTS
# =========================

from src.vectorstore.faiss_store import load_index
from src.retrieval.search import search
from src.generation.llm import generate_answer

# =========================
# FILE PATHS
# =========================

INDEX_PATH = PROJECT_ROOT / "data" / "vector_store" / "index.faiss"
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks" / "chunks.json"

# =========================
# SYSTEM LOADING (FAISS + CHUNKS)
# =========================

print("📦 Loading RAG system...")

index = load_index(INDEX_PATH)

if index is None:
    raise ValueError("❌ FAISS index could not be loaded correctly")

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks_list = json.load(f)

# Convert to index-based access
chunks = {i: chunk for i, chunk in enumerate(chunks_list)}

print("✔ System ready")

# =========================
# PROMPT BUILDER
# =========================

def build_prompt(question, results):

    context = "\n\n".join([
        f"[Source: {r['file']}]\n{r['text']}"
        for r in results
    ])

    # Deduplicate sources while preserving order
    sources = list(dict.fromkeys([r['file'] for r in results]))
    sources_list = "\n".join(f"- {s}" for s in sources)

    return f"""
You are a technical assistant specialized in pharmaceutical compliance documents.

Answer the question using ONLY the context provided below.
If the context contains relevant information, summarize and explain it clearly.
If the answer is truly not present in the context, respond:
"This information was not found in the available documents."

At the end of your answer, always include a "Sources" section listing only the documents from which you explicitly extracted information.

---

CONTEXT:
{context}

---

QUESTION:
{question}

---

ANSWER:
(your answer here)

Sources:
{sources_list}
"""


# =========================
# FULL RAG PIPELINE
# =========================

def answer(question):

    results = search(question, index, chunks)

    if not results:
        return "No relevant information found in the available documents."

    prompt = build_prompt(question, results)

    return generate_answer(prompt)

# =========================
# CLI INTERFACE (CHAT MODE)
# =========================

if __name__ == "__main__":

    print("\n🧠 Pharma Compliance Assistant ready (type 'exit' to quit)\n")

    while True:

        question = input("Ask a compliance question: ")

        if question.lower() == "exit":
            print("👋 Exiting...")
            break

        response = answer(question)

        print("\n🤖 Assistant:\n")
        print(response)
        print("\n" + "-" * 60)