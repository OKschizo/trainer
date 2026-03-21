"""MCP server providing deep expertise on the DWG binary file format.

This server exposes tools for querying the OpenDesign Specification for .dwg files,
enabling AI models to answer detailed questions about DWG file structure, data types,
compression algorithms, entity definitions, and more.
"""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from dwg_mcp.search import DwgSpecSearch

CHAPTERS_DIR = Path("knowledge/chapters")

mcp = FastMCP(
    "DWG Specification Expert",
    instructions=(
        "You are an expert on the DWG binary file format as documented in the "
        "OpenDesign Specification for .dwg files v5.4.1. Use the provided tools "
        "to search the specification and answer questions with precise, technical detail. "
        "Always cite section numbers and data types when answering."
    ),
)

_search: DwgSpecSearch | None = None


def _get_search() -> DwgSpecSearch:
    global _search
    if _search is None:
        _search = DwgSpecSearch()
    return _search


@mcp.tool()
def search_dwg_spec(query: str, n_results: int = 5) -> str:
    """Search the DWG file format specification using semantic search.

    Use this to find information about any aspect of the DWG binary format including:
    - Bit codes and data definitions (B, BB, BS, BL, BD, MC, MS, H, etc.)
    - File structure for specific DWG versions (R13-R15, R2004, R2007, R2010+)
    - Data sections (Header, Classes, Objects, Handles, Preview, etc.)
    - Entity and object definitions (LINE, CIRCLE, ARC, TEXT, MTEXT, etc.)
    - Compression algorithms (LZ77 variant used in R2004+)
    - Encryption and CRC calculations
    - Handle references and object maps
    - Reed-Solomon encoding (R2007+)

    Args:
        query: Natural language question about the DWG format.
        n_results: Number of relevant passages to return (1-20).
    """
    search = _get_search()
    n_results = max(1, min(20, n_results))
    results = search.search(query, n_results=n_results)

    if not results:
        return "No relevant passages found. Try rephrasing your query."

    output_parts = []
    for i, r in enumerate(results, 1):
        output_parts.append(
            f"--- Result {i} (source: {r['source']}, section: {r['section']}) ---\n"
            f"{r['text']}\n"
        )
    return "\n".join(output_parts)


@mcp.tool()
def get_dwg_chapter(chapter_number: int) -> str:
    """Retrieve a full chapter from the DWG specification.

    Available chapters:
     1: Introduction
     2: BIT CODES AND DATA DEFINITIONS
     3: R13-R15 DWG FILE FORMAT ORGANIZATION
     4: R2004 DWG FILE FORMAT ORGANIZATION
     5: R2007 DWG FILE FORMAT ORGANIZATION
     6: R2010 DWG FILE FORMAT ORGANIZATION
     7: R2013 DWG FILE FORMAT ORGANIZATION
     8: R2018 DWG FILE FORMAT ORGANIZATION
     9: Data section AcDb:Header (HEADER VARIABLES)
    10: Data section AcDb:Classes
    11: PADDING (R13C3 AND LATER)
    12: Data section: ""
    13: Data section AcDb:SummaryInfo
    14: Data section AcDb:Preview
    15: Data section AcDb:VBAProject
    16: Data section AcDb:AppInfo
    17: Data section AcDb:FileDepList
    18: Data section AcDb:RevHistory
    19: Data section AcDb:Security
    20: Data section AcDb:AcDbObjects
    21: Data section AcDb:ObjFreeSpace
    22: Data section AcDb:Template
    23: Data section AcDb:Handles (OBJECT MAP)
    24: Section AcDb:AcDsPrototype_1b (DataStorage)
    25: UNKNOWN SECTION
    26: SECOND FILE HEADER (R13-R15)
    27: Data section AcDb:AuxHeader
    28: Extended Entity Data
    29: PROXY ENTITY GRAPHICS

    Args:
        chapter_number: Chapter number (1-29).
    """
    if not CHAPTERS_DIR.exists():
        return "Error: chapters directory not found. Run 'dwg-extract' first."

    prefix = f"ch{chapter_number:02d}_"
    matches = list(CHAPTERS_DIR.glob(f"{prefix}*.md"))
    if not matches:
        return f"Chapter {chapter_number} not found. Valid range is 1-29."

    return matches[0].read_text(encoding="utf-8")


@mcp.tool()
def lookup_dwg_data_type(type_code: str) -> str:
    """Look up a DWG bit code / data type definition.

    Common DWG data types:
    B, BB, 3B, BS, BL, BLL, BD, 2BD, 3BD, RC, RS, RD, RL, 2RD, 3RD,
    MC, MS, H, T, TU, TV, X, U, SN, BE, DD, BT, 3DD, CMC, TC, OT, ENC

    Args:
        type_code: The type abbreviation (e.g. "BS", "H", "CMC", "MC").
    """
    search = _get_search()
    results = search.search(
        f"DWG data type definition {type_code} bit code format",
        n_results=3,
    )

    TYPE_DEFINITIONS = {
        "B": "bit (1 or 0)",
        "BB": "special 2 bit code (entmode in entities)",
        "3B": "bit triplet (1-3 bits) (R24)",
        "BS": "bitshort (16 bits). 00=short follows, 01=unsigned char follows, 10=0, 11=256",
        "BL": "bitlong (32 bits). 00=long follows, 01=unsigned char follows, 10=0, 11=not used",
        "BLL": "bitlonglong (64 bits) (R24). Length indicated by 3B, then that many bytes follow",
        "BD": "bitdouble. 00=double follows, 01=1.0, 10=0.0, 11=not used",
        "2BD": "2D point (2 bitdoubles)",
        "3BD": "3D point (3 bitdoubles)",
        "RC": "raw char (not compressed)",
        "RS": "raw short (not compressed)",
        "RD": "raw double (not compressed)",
        "RL": "raw long (not compressed)",
        "2RD": "2 raw doubles",
        "3RD": "3 raw doubles",
        "MC": "modular char - compressed integer, bytes until high bit is 0",
        "MS": "modular short - like MC but base module is a short",
        "H": "handle reference - CODE(4 bits) | COUNTER(4 bits) | HANDLE or OFFSET",
        "T": "text - bitshort length followed by the string",
        "TU": "Unicode text - bitshort char length followed by 2-byte-per-char Unicode string",
        "TV": "Variable text - T for <=R2004, TU for R2007+",
        "X": "special form",
        "U": "unknown",
        "SN": "16 byte sentinel",
        "BE": "BitExtrusion - R13-R14: 3BD. R2000+: 1 bit (1=0,0,1 assumed) else 3BD",
        "DD": (
            "BitDouble With Default - 2-bit opcode: "
            "00=default, 01=patch 4 bytes, 10=patch 6 bytes, 11=full RD"
        ),
        "BT": "BitThickness - R13-R14: BD. R2000+: 1 bit (1=0.0 assumed) else BD",
        "3DD": "3D point as 3 DD, needing 3 default values",
        "CMC": (
            "CmColor value - R15: BS color index. "
            "R2004+: BS(0) + BL(RGB) + RC(color byte with optional name/book)"
        ),
        "TC": "True Color - same as CMC in R2004+",
        "ENC": "Entity color with optional DBCOLOR ref and transparency",
        "OT": "Object type",
    }

    parts = []
    code_upper = type_code.upper()
    if code_upper in TYPE_DEFINITIONS:
        parts.append(f"**{code_upper}**: {TYPE_DEFINITIONS[code_upper]}\n")

    if results:
        parts.append("Relevant specification passages:")
        for r in results:
            parts.append(f"\n[{r['source']} - {r['section']}]\n{r['text']}")

    return "\n".join(parts) if parts else f"No definition found for '{type_code}'."


@mcp.tool()
def lookup_dwg_entity(entity_name: str) -> str:
    """Look up a DWG entity or object type definition.

    Common entities: LINE, POINT, CIRCLE, ARC, TEXT, MTEXT, SOLID, TRACE,
    INSERT, ATTRIB, ATTDEF, POLYLINE, VERTEX, SEQEND, DIMENSION, LEADER,
    LWPOLYLINE, HATCH, SPLINE, ELLIPSE, VIEWPORT, IMAGE, TABLE, etc.

    Common objects: DICTIONARY, DICTIONARYWDFLT, XRECORD, LAYOUT, BLOCK_HEADER,
    LAYER, STYLE, LTYPE, VIEW, UCS, VPORT, APPID, DIMSTYLE, MLINESTYLE, etc.

    Args:
        entity_name: Name of the entity or object (e.g. "CIRCLE", "MTEXT").
    """
    search = _get_search()
    results = search.search(
        f"DWG entity object {entity_name} definition structure fields",
        n_results=8,
    )

    if not results:
        return f"No specification data found for entity '{entity_name}'."

    parts = [f"## DWG Entity/Object: {entity_name.upper()}\n"]
    for i, r in enumerate(results, 1):
        parts.append(
            f"--- Passage {i} (source: {r['source']}, section: {r['section']}) ---\n"
            f"{r['text']}\n"
        )
    return "\n".join(parts)


@mcp.tool()
def lookup_dwg_version(version: str) -> str:
    """Get file format organization details for a specific DWG version.

    Supported versions: R13, R14, R15, R2000, R2004, R2007, R2010, R2013, R2018

    Version ID bytes (first 6 bytes of file):
    AC1012=R13, AC1014=R14, AC1015=R2000, AC1018=R2004,
    AC1021=R2007, AC1024=R2010, AC1027=R2013, AC1032=R2018

    Args:
        version: DWG version string (e.g. "R2004", "R2007").
    """
    search = _get_search()
    results = search.search(
        f"DWG {version} file format organization structure sections pages",
        n_results=8,
    )

    if not results:
        return f"No specification data found for version '{version}'."

    parts = [f"## DWG {version} File Format\n"]
    for i, r in enumerate(results, 1):
        parts.append(
            f"--- Passage {i} (source: {r['source']}, section: {r['section']}) ---\n"
            f"{r['text']}\n"
        )
    return "\n".join(parts)


@mcp.tool()
def list_indexed_chapters() -> str:
    """List all indexed chapters of the DWG specification."""
    search = _get_search()
    sources = search.list_sources()
    count = search.document_count

    parts = [
        f"DWG Specification Index ({count} chunks across {len(sources)} files)\n",
        "Available sources:",
    ]
    for src in sources:
        parts.append(f"  - {src}")
    return "\n".join(parts)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
