"""Tests for the AutoCAD PDF extraction pipeline."""

from scripts.extract_autocad_pdf import (
    build_chapter_documents,
    chapter_to_markdown,
    select_chapter_entries,
    slugify,
)


def test_slugify_normalizes_title():
    assert slugify("Door and Window Assemblies") == "door_and_window_assemblies"


def test_select_chapter_entries_prefers_level_two_outline():
    outline = [
        (1, "Contents", 3),
        (1, "Workflow and User Interface", 57),
        (2, "The Workspace", 83),
        (3, "The Ribbon", 88),
        (2, "Walls", 1145),
        (2, "Windows", 1941),
        (2, "Windows", 1941),
    ]

    chapters = select_chapter_entries(outline)

    assert chapters == [
        (1, "The Workspace", 83),
        (2, "Walls", 1145),
        (3, "Windows", 1941),
    ]


def test_chapter_to_markdown_includes_page_markers():
    markdown = chapter_to_markdown(
        chapter_number=2,
        chapter_title="Walls",
        page_start=10,
        page_end=11,
        page_lines=[
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["placeholder"],
            ["Walls", "Drawing Walls"],
            ["Editing Walls"],
        ],
    )

    assert "# Chapter 2: Walls" in markdown
    assert "<!-- pages: 10-10 -->" in markdown
    assert "## Page 10" in markdown
    assert "Editing Walls" in markdown


def test_build_chapter_documents_uses_outline(monkeypatch):
    monkeypatch.setattr(
        "scripts.extract_autocad_pdf.extract_outline",
        lambda _pdf: [
            (1, "Contents", 1),
            (2, "The Workspace", 5),
            (2, "Walls", 10),
        ],
    )
    monkeypatch.setattr(
        "scripts.extract_autocad_pdf.extract_page_lines",
        lambda _pdf: [
            ["Cover"],
            ["Contents"],
            ["Contents"],
            ["Contents"],
            ["Workspace intro"],
            ["Workspace details"],
            ["Workspace details"],
            ["Workspace details"],
            ["Workspace details"],
            ["Walls intro"],
            ["Walls details"],
        ],
    )

    docs = build_chapter_documents(pdf_path=None)  # type: ignore[arg-type]

    assert len(docs) == 2
    assert docs[0]["source"].startswith("ch01_the_workspace")
    assert docs[0]["page_start"] == 5
    assert docs[0]["page_end"] == 9
    assert docs[1]["source"].startswith("ch02_walls")
    assert docs[1]["page_start"] == 10
