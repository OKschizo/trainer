"""Tests for the PDF extraction pipeline."""


from scripts.extract_pdf import clean_text, split_into_chapters


def test_clean_text_removes_headers():
    text = "Open Design Specification for .dwg files 42\nSome content here"
    cleaned = clean_text(text)
    assert "42" not in cleaned or "Some content here" in cleaned


def test_clean_text_removes_page_markers():
    text = "Some data\n-- 5 of 279 --\nMore data"
    cleaned = clean_text(text)
    assert "-- 5 of 279 --" not in cleaned
    assert "Some data" in cleaned
    assert "More data" in cleaned


def test_split_into_chapters_finds_known():
    text = (
        "\n1 Introduction\nSome intro text.\n"
        "\n2 BIT CODES AND DATA DEFINITIONS\nBit code info.\n"
    )
    chapters = split_into_chapters(text)
    assert len(chapters) >= 1
    assert any(c[0] == 1 for c in chapters)
