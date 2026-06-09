# =========================
# STREAMLIT APP
# =========================
# Pharma Compliance RAG Assistant
# Web interface for the RAG pipeline

import streamlit as st
import sys
import json
from pathlib import Path

# =========================
# PROJECT CONFIGURATION
# =========================

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.vectorstore.faiss_store import load_index
from src.retrieval.search import search
from src.generation.llm import generate_answer

# =========================
# FILE PATHS
# =========================

INDEX_PATH = PROJECT_ROOT / "data" / "vector_store" / "index.faiss"
CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks" / "chunks.json"

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Pharma Compliance Assistant",
    page_icon="💊",
    layout="centered"
)

# =========================
# DOWNLOAD DATA FROM HUGGING FACE
# =========================

def download_data_from_hf():
    from huggingface_hub import hf_hub_download
    import os

    HF_REPO = "PipetteAndPython/pharma-compliance-docs"

    # Create directories if they don't exist
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Download FAISS index
    if not INDEX_PATH.exists():
        hf_hub_download(
            repo_id=HF_REPO,
            repo_type="dataset",
            filename="vector_store/index.faiss",
            local_dir=PROJECT_ROOT / "data"
        )

    # Download chunks
    if not CHUNKS_PATH.exists():
        hf_hub_download(
            repo_id=HF_REPO,
            repo_type="dataset",
            filename="chunks/chunks.json",
            local_dir=PROJECT_ROOT / "data"
        )


# =========================
# LOAD RAG SYSTEM (CACHED)
# =========================
# @st.cache_resource ensures FAISS and chunks are loaded only once
# and reused across all user interactions

@st.cache_resource
def load_rag_system():
    download_data_from_hf()
    index = load_index(INDEX_PATH)
    if index is None:
        raise ValueError("❌ FAISS index could not be loaded.")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks_list = json.load(f)
    chunks = {i: chunk for i, chunk in enumerate(chunks_list)}
    return index, chunks

# =========================
# PROMPT BUILDER
# =========================

def build_prompt(question, results):

    context = "\n\n".join([
        f"[Source: {r['file']}]\n{r['text']}"
        for r in results
    ])

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
# RAG PIPELINE
# =========================

def answer(question, index, chunks):
    results = search(question, index, chunks)
    if not results:
        return "No relevant information found in the available documents."
    prompt = build_prompt(question, results)
    return generate_answer(prompt)

# =========================
# SIDEBAR
# =========================

with st.sidebar:
    st.title("💊 Pharma Compliance Assistant")
    st.markdown(
        "This assistant answers questions based on a curated collection of "
        "pharmaceutical regulatory documents including ICH guidelines, "
        "FDA regulations, EMA guidance, and ANMAT dispositions."
    )
    st.divider()
    st.markdown("**Regulatory sources include:**")
    st.markdown("- ICH Q8, Q9, Q10, Q11, Q12, Q13")
    st.markdown("- FDA 21 CFR Parts 210/211")
    st.markdown("- EMA Guidelines")
    st.markdown("- ANMAT Dispositions")
    st.divider()
    st.caption("Answers are based solely on indexed documents. Always consult a qualified regulatory professional.")

# =========================
# MAIN INTERFACE
# =========================

st.title("💊 Pharma Compliance Assistant")
st.caption("Ask questions about GMP, ICH guidelines, FDA regulations, and more.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load RAG system
try:
    index, chunks = load_rag_system()
except Exception as e:
    st.error(f"❌ Error loading RAG system: {e}")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if question := st.chat_input("Ask a compliance question..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # Add to history
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching documents..."):
            response = answer(question, index, chunks)
        st.markdown(response)

    # Add response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })