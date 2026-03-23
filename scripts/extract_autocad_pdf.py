"""Extract an AutoCAD user guide PDF into markdown chapters."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import click
import fitz  # pymupdf

DEFAULT_PDF = Path("autocad_aca_user_guide_englishCOMP2.pdf")
DEFAULT_OUTPUT_DIR = Path("knowledge/autocad_chapters")
HEADING_MAX_LENGTH = 120


def slugify(value: str) -> str:
    """Convert a title into a filename-safe slug."""
    cleaned = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "_", cleaned)[:80] or "untitled"


def normalize_line(line: str) -> str:
    """Normalize whitespace and remove table-of-contents dot leaders."""
    line = line.replace("\x00", " ")
    line = re.sub(r"\s+", " ", line).strip()
    line = re.sub(r"\s?\.{3,}\s?\d+$", "", line).strip()
    return line


def clean_page_text(text: str) -> list[str]:
    """Normalize text extracted from a single PDF page."""
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = normalize_line(raw_line)
        if not line:
            continue
        if line == "Contents":
            lines.append(line)
            continue
        if len(line) > 220:
            lines.append(line)
            continue
        lines.append(line)
    return lines


def extract_outline(pdf_path: Path) -> list[tuple[int, str, int]]:
    """Return the PDF outline as (level, title, page_number) entries."""
    doc = fitz.open(str(pdf_path))
    toc = doc.get_toc(simple=True)
    doc.close()
    return [
        (level, title.strip(), page_number)
        for level, title, page_number in toc
        if title.strip()
    ]


def select_chapter_entries(outline: Iterable[tuple[int, str, int]]) -> list[tuple[int, str, int]]:
    """Select top-level chapter entries from a PDF outline."""
    entries = list(outline)
    if not entries:
        return []

    # AutoCAD manuals often use level 1 for book sections and level 2 for chapters.
    candidates = [entry for entry in entries if entry[0] == 2]
    if not candidates:
        candidates = [entry for entry in entries if entry[0] == 1]

    chapter_entries: list[tuple[int, str, int]] = []
    seen: set[tuple[str, int]] = set()
    for _level, title, page in candidates:
        normalized = title.strip()
        if len(normalized) > HEADING_MAX_LENGTH:
            continue
        if normalized.lower() == "contents":
            continue
        key = (normalized.lower(), page)
        if key in seen:
            continue
        seen.add(key)
        chapter_entries.append((len(chapter_entries) + 1, normalized, page))
    return chapter_entries


def extract_page_lines(pdf_path: Path) -> list[list[str]]:
    """Extract normalized text lines for every PDF page."""
    doc = fitz.open(str(pdf_path))
    pages = [clean_page_text(page.get_text("text")) for page in doc]
    doc.close()
    return pages


def chapter_to_markdown(
    chapter_number: int,
    chapter_title: str,
    page_start: int,
    page_end: int,
    page_lines: list[list[str]],
) -> str:
    """Render extracted chapter pages as markdown."""
    lines = [
        f"# Chapter {chapter_number}: {chapter_title}",
        "",
        f"_Source pages: {page_start}-{page_end}_",
        f"<!-- pages: {page_start}-{page_end} -->",
        "",
    ]

    for page_number in range(page_start, page_end + 1):
        lines.append(f"<!-- pages: {page_number}-{page_number} -->")
        lines.append(f"## Page {page_number}")
        lines.append("")
        for line in page_lines[page_number - 1]:
            lines.append(line)
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_chapter_documents(pdf_path: Path) -> list[dict]:
    """Build chapter markdown documents from the AutoCAD PDF."""
    outline = extract_outline(pdf_path)
    chapter_entries = select_chapter_entries(outline)
    if not chapter_entries:
        raise ValueError("No suitable chapter entries found in the PDF outline.")

    page_lines = extract_page_lines(pdf_path)
    page_count = len(page_lines)
    documents: list[dict] = []

    for index, (chapter_number, title, page_start) in enumerate(chapter_entries):
        if index + 1 < len(chapter_entries):
            page_end = chapter_entries[index + 1][2] - 1
        else:
            page_end = page_count
        page_end = max(page_start, min(page_end, page_count))
        source = f"ch{chapter_number:02d}_{slugify(title)}.md"
        documents.append(
            {
                "chapter_number": chapter_number,
                "title": title,
                "page_start": page_start,
                "page_end": page_end,
                "source": source,
                "markdown": chapter_to_markdown(
                    chapter_number=chapter_number,
                    chapter_title=title,
                    page_start=page_start,
                    page_end=page_end,
                    page_lines=page_lines,
                ),
            }
        )
    return documents


@click.command()
@click.option(
    "--pdf",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_PDF,
    help="Path to the AutoCAD user guide PDF.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=DEFAULT_OUTPUT_DIR,
    help="Directory to write markdown chapter files.",
)
def main(pdf: Path, output_dir: Path) -> None:
    """Extract the AutoCAD guide PDF into chapter markdown files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    click.echo(f"Reading PDF outline from {pdf}...")
    documents = build_chapter_documents(pdf)
    click.echo(f"Found {len(documents)} chapter entries")

    for document in documents:
        destination = output_dir / document["source"]
        destination.write_text(document["markdown"], encoding="utf-8")
        click.echo(
            f"  Wrote {destination.name} "
            f"(pages {document['page_start']}-{document['page_end']})"
        )

    click.echo(f"\nDone! Extracted {len(documents)} AutoCAD chapters to {output_dir}")


if __name__ == "__main__":
    main()
