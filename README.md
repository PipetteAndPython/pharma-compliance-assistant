# 💊 Pharma Compliance Assistant

A RAG-based (Retrieval-Augmented Generation) assistant for pharmaceutical regulatory compliance. Ask questions about GMP, ICH guidelines, FDA regulations, EMA guidance, ANMAT dispositions, and more — and get answers grounded in the actual regulatory documents.

🔗 **Live Demo**: [pharma-compliance-assistant-9rsrbbatypsuwsyb89yjhi.streamlit.app](https://pharma-compliance-assistant-9rsrbbatypsuwsyb89yjhi.streamlit.app/)

---

## 🧠 What it does

This assistant allows users to ask natural language questions about pharmaceutical compliance and receive answers based on a curated collection of regulatory documents. It does not rely on general AI knowledge — every answer is grounded in the indexed documents and includes citations.

---

## 📚 Regulatory Sources

The knowledge base includes documents from:

- **ICH Guidelines**: Q7, Q8, Q9, Q10, Q11, Q12, Q13 and associated training materials
- **FDA Regulations**: 21 CFR Title 21 (multiple volumes)
- **EMA Guidelines**
- **ANMAT Dispositions**


---

## 🏗️ Architecture

```
PHARMA_PROJECT/               #HuggingFace
│
├── data/
│   ├── raw/                  # original documents (HuggingFace)
│   ├── chunks/               # chunks.json (HuggingFace)
│   ├── vector_store/         # index.faiss (HuggingFace)
```
=========================================================
```
PHARMA_PROJECT/
│
├── data/
│   └── registry.json         # Tracks processed documents (incremental builds)
│
├── app/
│   ├── build.py              # Offline pipeline: documents → chunks → embeddings → FAISS
│   ├── query.py              # Debug tool: semantic search without LLM
│   └── rag_assistant.py      # Full RAG pipeline + CLI interface
│
├── src/
│   ├── ingestion/
│   │   └── doc_loader.py     # Loads PDF, DOCX, PPTX documents
│   ├── processing/
│   │   ├── text_splitter.py  # Chunks text with overlap
│   │   └── embeddings.py     # Generates embeddings (sentence-transformers)
│   ├── vectorstore/
│   │   └── faiss_store.py    # Builds, saves, and loads FAISS index
│   ├── retrieval/
│   │   └── search.py         # Semantic search over FAISS
│   └── generation/
│       └── llm.py            # Groq LLM interface
│
└── streamlit_app.py          # Web interface
```


## ⚙️ How it works

1. **Ingestion**: Documents (PDF, DOCX, PPTX) are loaded and converted to plain text
2. **Chunking**: Text is split into overlapping fragments to preserve context
3. **Embeddings**: Each chunk is converted into a semantic vector using `all-MiniLM-L6-v2`
4. **Indexing**: Vectors are stored in a FAISS index for fast similarity search
5. **Retrieval**: User questions are embedded and matched against the index
6. **Generation**: Relevant chunks are passed to a Groq LLM (llama-3.1-8b-instant) to generate a grounded answer with source citations

---

## 🔄 Incremental Build System

The system tracks which documents have already been processed in `data/registry.json`. When new documents are added to the knowledge base, only the new ones are processed — saving significant time and compute.

---

## 🗄️ Data Storage

| Data | Location |
|------|----------|
| Raw documents (PDF, DOCX, PPTX) | [Hugging Face Dataset](https://huggingface.co/datasets/PipetteAndPython/pharma-compliance-docs) |
| Chunks (chunks.json) | Hugging Face Dataset |
| FAISS index (index.faiss) | Hugging Face Dataset |
| Document registry | GitHub |
| Source code | GitHub |

---

## 🚀 Run locally

```bash
# Clone the repository
git clone https://github.com/PipetteAndPython/pharma-compliance-assistant.git
cd pharma-compliance-assistant

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY="your-key-here"  # Mac/Linux
set GROQ_API_KEY="your-key-here"     # Windows

# Build the RAG index (downloads data from Hugging Face)
python app/build.py

# Run the web interface
streamlit run streamlit_app.py

# Or use the CLI
python app/rag_assistant.py
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Vector search | FAISS |
| LLM | Groq (llama-3.1-8b-instant) |
| Document loading | pypdf, python-docx, python-pptx |
| Web interface | Streamlit |
| Data storage | Hugging Face Datasets |

---

## 📝 Notes

- Answers are based solely on the indexed regulatory documents
- Built as a final project for [Code in Place](https://codeinplace.stanford.edu/) — Stanford University's introductory Python course
