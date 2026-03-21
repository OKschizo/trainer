# AGENTS.md

## Cursor Cloud specific instructions

This is a Python MCP server providing DWG file format expertise via RAG. See `README.md` for full docs.

### Key commands

- **Install deps:** `pip install -e ".[dev]"` (run from venv)
- **Lint:** `ruff check src/ scripts/ tests/`
- **Tests:** `PYTHONPATH=src pytest tests/ -v`
- **Extract PDF:** `python scripts/extract_pdf.py` (requires PDF in `knowledge/raw/`)
- **Build index:** `python scripts/build_index.py` (requires extracted chapters)
- **Run MCP server:** `PYTHONPATH=src python -m dwg_mcp.server`

### Non-obvious caveats

- The vector DB (`knowledge/vectordb/`) and raw PDF (`knowledge/raw/*.pdf`) are git-ignored. The extraction and indexing pipeline must be run before the MCP server or search tests will work.
- `PYTHONPATH=src` is required when running tests or the server, since the `dwg_mcp` package lives under `src/`.
- The `sentence-transformers` model (`all-MiniLM-L6-v2`) downloads on first use (~90MB). Subsequent runs use the cached model.
- ChromaDB's `SentenceTransformerEmbeddingFunction` may show a `LOAD REPORT` warning about `embeddings.position_ids` being unexpected — this is harmless and can be ignored.
- Chapter extraction matches headings after the Table of Contents to avoid capturing ToC entries.
