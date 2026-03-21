"""Demo script to verify the DWG specification search works end-to-end."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from dwg_mcp.search import DwgSpecSearch


def main():
    print("=" * 70)
    print("DWG Specification Expert - Demo Search")
    print("=" * 70)

    search = DwgSpecSearch()
    print(f"\nIndex loaded: {search.document_count} chunks\n")

    queries = [
        "How is a BITSHORT encoded in the DWG format?",
        "What is the structure of a handle reference?",
        "How does R2004 compression work?",
        "What fields does a CIRCLE entity contain?",
        "What are the first 6 bytes of a DWG file?",
    ]

    for query in queries:
        print(f"\n{'─' * 70}")
        print(f"Q: {query}")
        print(f"{'─' * 70}")
        results = search.search(query, n_results=2)
        for i, r in enumerate(results, 1):
            preview = r["text"][:300].replace("\n", " ")
            print(f"\n  [{i}] ({r['source']} | {r['section']})")
            print(f"      {preview}...")

    print(f"\n{'=' * 70}")
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
