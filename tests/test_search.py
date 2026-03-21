"""Integration tests for the DWG specification search engine."""

from pathlib import Path

import pytest

from dwg_mcp.search import DwgSpecSearch

DB_PATH = Path("knowledge/vectordb")


@pytest.fixture(scope="module")
def search():
    if not DB_PATH.exists():
        pytest.skip("Vector DB not built; run 'python scripts/build_index.py' first")
    return DwgSpecSearch(db_path=DB_PATH)


def test_search_returns_results(search):
    results = search.search("bitshort data type encoding")
    assert len(results) > 0
    assert "text" in results[0]
    assert "source" in results[0]


def test_search_bit_codes(search):
    results = search.search("How is a BITSHORT encoded in DWG files?")
    combined = " ".join(r["text"] for r in results)
    assert "bitshort" in combined.lower() or "BS" in combined


def test_search_handles(search):
    results = search.search("handle reference format CODE COUNTER")
    combined = " ".join(r["text"] for r in results)
    assert "handle" in combined.lower() or "COUNTER" in combined


def test_search_compression(search):
    results = search.search("LZ77 compression algorithm R2004")
    combined = " ".join(r["text"] for r in results)
    assert "compress" in combined.lower()


def test_search_entity(search):
    results = search.search("CIRCLE entity definition DWG")
    assert len(results) > 0


def test_list_sources(search):
    sources = search.list_sources()
    assert len(sources) > 0
    assert any("ch02" in s for s in sources)


def test_document_count(search):
    assert search.document_count > 100
