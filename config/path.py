from pathlib import Path

# =========================
# ROOT DEL PROYECTO
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# =========================
# DATA PATHS
# =========================
DATA_DIR = PROJECT_ROOT / "data"

RAW_PATH = DATA_DIR / "raw"
CHUNKS_PATH = DATA_DIR / "chunks" / "chunks.json"
INDEX_PATH = DATA_DIR / "vector_store" / "index.faiss"
REGISTRY_PATH = DATA_DIR / "processed" / "indexed_files.json"