# =========================
# BUILD PIPELINE (OFFLINE)
# =========================
# This script runs ONLY when you want to build or rebuild the RAG system.
# Flow:
#   Documents → chunks → embeddings → FAISS → saved to disk
#
# NOT executed on every query (that is handled by query.py)

import sys
import os
import json

from pathlib import Path
# Modern library for cross-platform path handling
# Replaces os.path and avoids path errors on Windows/Linux/Mac

# =========================
# PROJECT ROOT CONFIGURATION
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
# __file__ → path of the current file (app/build.py)
# .resolve() → converts to absolute path (avoids ambiguous relative paths)
# .parents[1] →
#     parents[0] = "app" folder
#     parents[1] = project root folder (PHARMA_PROJECT)
# Result: PROJECT_ROOT always points to the project root regardless of terminal location

# =========================
# BASE PATH DEFINITIONS
# =========================

RAW_PATH = PROJECT_ROOT / "data" / "raw"
# Path to original documents (PDFs, DOCX, PPTX)
# Equivalent to: PHARMA_PROJECT/data/raw
# The "/" operator in pathlib safely concatenates paths

CHUNKS_PATH = PROJECT_ROOT / "data" / "chunks" / "chunks.json"
# Path where processed chunks are saved in JSON format
# Equivalent to: PHARMA_PROJECT/data/chunks/chunks.json
# Stores divided text fragments to avoid reprocessing

INDEX_PATH = PROJECT_ROOT / "data" / "vector_store" / "index.faiss"
# Path where the FAISS index is saved
# Equivalent to: PHARMA_PROJECT/data/vector_store/index.faiss
# Contains the vector database for fast semantic search

registry_path = PROJECT_ROOT / "data" / "registry.json"

# =========================
# PROJECT IMPORTS
# =========================

from src.ingestion.doc_loader import load_documents
# Reads all documents from data/raw and converts them to text

from src.processing.text_splitter import chunk_text
# Splits long texts into smaller fragments (chunks)

from src.processing.embeddings import create_embeddings
# Converts each chunk into a numerical vector (embedding)

from src.vectorstore.faiss_store import (
    build_faiss_index,
    save_index,
    load_index
)
# FAISS index management:
# - build
# - save
# - load existing index


# =========================
# 1. DOCUMENT LOADING (INCREMENTAL)
# =========================
# Reads new documents from data/raw and skips already indexed ones.

print("🔄 Loading documents (PDF, DOCX, PPTX)...")

docs = load_documents(RAW_PATH)

if not docs:
    print("⚠ No documents found in data/raw. Please check the folder.")
    sys.exit(0)

# =========================
# LOAD PROCESSED FILES REGISTRY
# =========================
# This file tracks which documents have already been processed.

if registry_path.exists() and registry_path.stat().st_size > 0:
    with open(registry_path, "r", encoding="utf-8") as f:
        processed_files = set(json.load(f))
else:
    processed_files = set()


# =========================
# FILTER NEW DOCUMENTS ONLY
# =========================
# Keep only documents that have not been indexed yet.

new_docs = [d for d in docs if d["file"] not in processed_files]

print(f"✔ Documents detected: {len(docs)}")
print(f"🆕 New documents: {len(new_docs)}")


# =========================
# 2. CHUNK CREATION
# =========================
# Splits each document into smaller fragments.
# Only new documents are processed.

print("🔄 Generating chunks...")

# Load existing chunks if any
if CHUNKS_PATH.exists():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        existing_chunks = json.load(f)
else:
    existing_chunks = []

# Generate chunks only for new documents
all_chunks = []

for doc in new_docs:
    chunks = chunk_text(doc["text"])
    for chunk in chunks:
        all_chunks.append({
            "file": doc["file"],
            "text": chunk
        })

print(f"✔ Chunks generated: {len(all_chunks)}")

# Combine existing + new chunks and save
print("💾 Saving chunks...")

CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

all_chunks_to_save = existing_chunks + all_chunks

with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
    json.dump(all_chunks_to_save, f, ensure_ascii=False, indent=2)

print(f"✔ chunks.json updated ({len(existing_chunks)} existing + {len(all_chunks)} new)")

# =========================
# 3. EMBEDDING CREATION
# =========================
# Converts each new chunk into a semantic vector.
# Only chunks from new documents are processed.

print("🧠 Creating embeddings...")

# Generate one embedding per chunk
# Result is a numerical representation of the text
embeddings = create_embeddings(all_chunks)

print("✔ Embeddings created")


# =========================
# 4. BUILD / UPDATE FAISS INDEX
# =========================
# If index already exists:
#   → load it and add new embeddings
#
# If it does not exist:
#   → create a new index from scratch

print("📦 Updating FAISS index...")

index_updated = False

if len(embeddings) == 0:
    print("ℹ No new embeddings. FAISS index will not be updated.")

else:
    if INDEX_PATH.exists():
        print("📂 Existing index detected")
        index = load_index(INDEX_PATH)
        index.add(embeddings)
        print("✔ New embeddings added to index")
    else:
        print("🆕 Creating new FAISS index")
        index = build_faiss_index(embeddings)
        print("✔ FAISS index created")

    index_updated = True


# =========================
# 5. SAVE FAISS INDEX
# =========================
# Saves the updated index to disk

print("💾 Saving FAISS index...")

if index_updated:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_index(index, INDEX_PATH)
    print("✔ Index saved")
else:
    print("ℹ No index to save (no changes)")


# =========================
# 6. UPDATE REGISTRY
# =========================
# Saves which documents have already been processed

print("📝 Updating document registry...")

# Add new files to the existing registry
processed_files.update(d["file"] for d in new_docs)

# Save updated registry
with open(registry_path, "w", encoding="utf-8") as f:
    json.dump(list(processed_files), f, indent=2)

print("✔ Registry updated")

# =========================
# 7. BUILD COMPLETE
# =========================

print("\n🎉 BUILD COMPLETE - System ready for queries")
print("You can now run: app/rag_assistant.py")