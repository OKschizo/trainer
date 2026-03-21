"""Tests for the chunking logic."""

from scripts.build_index import chunk_text


def test_chunk_text_basic():
    text = "Line one\nLine two\nLine three\nLine four\n" * 50
    chunks = chunk_text(text, source="test.md", chunk_size=200, chunk_overlap=50)
    assert len(chunks) > 1

    for chunk in chunks:
        assert "id" in chunk
        assert "text" in chunk
        assert "source" in chunk
        assert chunk["source"] == "test.md"


def test_chunk_text_small_input():
    text = "Short text."
    chunks = chunk_text(text, source="small.md", chunk_size=1000)
    assert len(chunks) == 1
    assert chunks[0]["text"] == "Short text."


def test_chunk_preserves_section():
    text = "## 2.1 Bitshort\nSome explanation\n" * 100
    chunks = chunk_text(text, source="test.md", chunk_size=200)
    for chunk in chunks:
        assert chunk["section"] != "" or chunk == chunks[0]
