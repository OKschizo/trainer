# DWG + AutoCAD MCP Servers

This repository now contains two separate MCP (Model Context Protocol) servers:

- `dwg_mcp`: deep expertise on the **DWG binary file format** via RAG over the OpenDesign DWG specification.
- `autocad_mcp`: product-design guidance for building a browser-operable, open-source **AutoCAD-like application** using the AutoCAD Architecture user guide as source material.

## What it does

### DWG MCP

The DWG pipeline turns the 279-page OpenDesign DWG specification into a searchable knowledge base that AI models can query through MCP tools. It covers:

- **Bit codes & data types** — B, BB, BS, BL, BD, MC, MS, H, CMC, etc.
- **File format versions** — R13 through R2018
- **File structure** — headers, sections, pages, encryption, compression
- **All entity/object definitions** — LINE, CIRCLE, ARC, TEXT, MTEXT, POLYLINE, HATCH, INSERT, DIMENSION, etc.
- **Compression** — LZ77 variant (R2004+), Reed-Solomon encoding (R2007+)
- **Encryption & CRC** — 8-bit/32-bit CRC, 64-bit CRC, data encryption schemes

### AutoCAD MCP

The AutoCAD pipeline turns the AutoCAD Architecture user guide into a searchable planning knowledge base that AI agents can use to scope and implement browser CAD functionality. It supports:

- **Manual search** — retrieve relevant passages for UI, workflows, and object behavior
- **Feature planning** — build implementation briefs for features like walls, windows, roofs, layers, and drawing management
- **Workflow mapping** — extract command flows, creation/edit steps, and follow-up operations
- **Chapter retrieval** — inspect full extracted chapters from the user guide

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
- Python 3.11+
- The OpenDesign DWG specification PDF for the DWG MCP
- The AutoCAD user guide PDF for the AutoCAD MCP

### Setup

```bash
# Create virtual environment and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# DWG MCP
python3 scripts/extract_pdf.py
python3 scripts/build_index.py
PYTHONPATH=src python3 -m dwg_mcp.server

# AutoCAD MCP
python3 scripts/extract_autocad_pdf.py --pdf autocad_aca_user_guide_englishCOMP2.pdf
python3 scripts/build_autocad_index.py
PYTHONPATH=src python3 -m autocad_mcp.server
```

### AutoCAD MCP tools

The AutoCAD server exposes these tools:

| Tool | Description |
|------|-------------|
| `search_autocad_manual` | Semantic search across the indexed AutoCAD guide |
| `get_autocad_chapter` | Retrieve a full extracted chapter by slug/prefix |
| `list_autocad_sources` | List all indexed AutoCAD chapter files |
| `plan_autocad_feature` | Build a manual-grounded implementation brief for a feature |
| `map_autocad_workflow` | Build a workflow checklist from the user guide |

### DWG MCP tools

The server exposes these tools:

| Tool | Description |
|------|-------------|
| `search_dwg_spec` | Semantic search across the entire specification |
| `get_dwg_chapter` | Retrieve a full chapter (1-29) |
| `lookup_dwg_data_type` | Look up a bit code type (BS, H, CMC, etc.) |
| `lookup_dwg_entity` | Look up an entity/object definition (CIRCLE, MTEXT, etc.) |
| `lookup_dwg_version` | Get format details for a specific DWG version |
| `list_indexed_chapters` | List all indexed chapters and chunk count |

### Cursor MCP configuration

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "dwg-spec": {
      "command": "python3",
      "args": ["-m", "dwg_mcp.server"],
      "cwd": "/path/to/this/repo",
      "env": {
        "PYTHONPATH": "src"
      }
    },
    "autocad-design": {
      "command": "python3",
      "args": ["-m", "autocad_mcp.server"],
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
├── src/dwg_mcp/              # DWG file-format MCP server
├── src/autocad_mcp/          # AutoCAD design-planning MCP server
├── scripts/
│   ├── extract_pdf.py         # DWG PDF → markdown chapters
│   ├── build_index.py         # DWG ChromaDB index
│   ├── extract_autocad_pdf.py # AutoCAD PDF → markdown chapters
│   └── build_autocad_index.py # AutoCAD ChromaDB index
├── knowledge/
│   ├── raw/                   # DWG source PDF (git-ignored)
│   ├── chapters/              # DWG extracted markdown chapters
│   ├── vectordb/              # DWG ChromaDB store (git-ignored)
│   ├── autocad_chapters/      # AutoCAD extracted markdown chapters (git-ignored)
│   └── autocad_vectordb/      # AutoCAD ChromaDB store (git-ignored)
├── tests/                     # pytest test suite
├── pyproject.toml             # Project config and dependencies
└── README.md
```
