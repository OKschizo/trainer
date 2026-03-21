# DWG Specification MCP Server

An MCP (Model Context Protocol) server that provides deep expertise on the **DWG binary file format** via RAG (Retrieval Augmented Generation) over the [OpenDesign Specification for .dwg files v5.4.1](https://www.opendesign.com/).

## What it does

This project turns the 279-page OpenDesign DWG specification into a searchable knowledge base that AI models can query through MCP tools. It covers:

- **Bit codes & data types** — B, BB, BS, BL, BD, MC, MS, H, CMC, etc.
- **File format versions** — R13 through R2018
- **File structure** — headers, sections, pages, encryption, compression
- **All entity/object definitions** — LINE, CIRCLE, ARC, TEXT, MTEXT, POLYLINE, HATCH, INSERT, DIMENSION, etc.
- **Compression** — LZ77 variant (R2004+), Reed-Solomon encoding (R2007+)
- **Encryption & CRC** — 8-bit/32-bit CRC, 64-bit CRC, data encryption schemes

## Architecture

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│   AI Model   │◄───►│   MCP Server    │◄───►│  ChromaDB    │
│ (Claude etc) │     │  (FastMCP)      │     │  Vector DB   │
└──────────────┘     └─────────────────┘     └──────────────┘
                            │                       ▲
                            │                       │
                     ┌──────┴──────┐        ┌───────┴────────┐
                     │  Chapter    │        │  Embedding     │
                     │  Files (.md)│───────►│  Pipeline      │
                     └─────────────┘        └────────────────┘
                            ▲
                     ┌──────┴──────┐
                     │  PDF        │
                     │  Extractor  │
                     └─────────────┘
```

## Quick start

### Prerequisites

- Python 3.11+
- The OpenDesign Specification PDF (place in `knowledge/raw/`)

### Setup

```bash
# Create virtual environment and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Step 1: Extract PDF into structured markdown chapters
python scripts/extract_pdf.py

# Step 2: Build the vector search index
python scripts/build_index.py

# Step 3: Run the MCP server
python -m dwg_mcp.server
```

### MCP Tools

The server exposes these tools:

| Tool | Description |
|------|-------------|
| `search_dwg_spec` | Semantic search across the entire specification |
| `get_dwg_chapter` | Retrieve a full chapter (1-29) |
| `lookup_dwg_data_type` | Look up a bit code type (BS, H, CMC, etc.) |
| `lookup_dwg_entity` | Look up an entity/object definition (CIRCLE, MTEXT, etc.) |
| `lookup_dwg_version` | Get format details for a specific DWG version |
| `list_indexed_chapters` | List all indexed chapters and chunk count |

### Cursor MCP Configuration

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "dwg-spec": {
      "command": "python",
      "args": ["-m", "dwg_mcp.server"],
      "cwd": "/path/to/this/repo",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

## Development

```bash
# Run tests
PYTHONPATH=src pytest tests/ -v

# Lint
ruff check src/ scripts/ tests/

# Format
ruff format src/ scripts/ tests/
```

## Project structure

```
├── src/dwg_mcp/          # MCP server package
│   ├── server.py          #   FastMCP server with DWG tools
│   └── search.py          #   ChromaDB semantic search engine
├── scripts/
│   ├── extract_pdf.py     # PDF → structured markdown chapters
│   └── build_index.py     # Build ChromaDB vector index
├── knowledge/
│   ├── raw/               # Source PDF (git-ignored)
│   ├── chapters/          # Extracted markdown chapters
│   └── vectordb/          # ChromaDB persistent store (git-ignored)
├── tests/                 # pytest test suite
├── pyproject.toml         # Project config and dependencies
└── README.md
```
