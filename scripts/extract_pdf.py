"""Extract the OpenDesign DWG specification PDF into structured markdown chapters."""

from __future__ import annotations

import re
from pathlib import Path

import click
import fitz  # pymupdf

CHAPTER_PATTERN = re.compile(
    r"^(\d+(?:\.\d+)*)\s+(.+)$", re.MULTILINE
)

TOP_LEVEL_CHAPTERS = [
    (1, "Introduction"),
    (2, "BIT CODES AND DATA DEFINITIONS"),
    (3, "R13-R15 DWG FILE FORMAT ORGANIZATION"),
    (4, "R2004 DWG FILE FORMAT ORGANIZATION"),
    (5, "R2007 DWG FILE FORMAT ORGANIZATION"),
    (6, "R2010 DWG FILE FORMAT ORGANIZATION"),
    (7, "R2013 DWG FILE FORMAT ORGANIZATION"),
    (8, "R2018 DWG FILE FORMAT ORGANIZATION"),
    (9, "Data section AcDb:Header (HEADER VARIABLES)"),
    (10, "Data section AcDb:Classes"),
    (11, "PADDING (R13C3 AND LATER)"),
    (12, 'Data section: ""'),
    (13, "Data section AcDb:SummaryInfo Section"),
    (14, "Data section AcDb:Preview"),
    (15, "Data section AcDb:VBAProject Section"),
    (16, "Data section AcDb:AppInfo"),
    (17, "Data section AcDb:FileDepList"),
    (18, "Data section AcDb:RevHistory"),
    (19, "Data section AcDb:Security"),
    (20, "Data section AcDb:AcDbObjects"),
    (21, "Data section AcDb:ObjFreeSpace"),
    (22, "Data section: AcDb:Template"),
    (23, "Data section AcDb:Handles (OBJECT MAP)"),
    (24, "Section AcDb:AcDsPrototype_1b (DataStorage)"),
    (25, "UNKNOWN SECTION"),
    (26, "SECOND FILE HEADER (R13-R15)"),
    (27, "Data section: AcDb:AuxHeader (Auxiliary file header)"),
    (28, "Extended Entity Data (Extended Object Data)"),
    (29, "PROXY ENTITY GRAPHICS"),
]


def extract_full_text(pdf_path: Path) -> str:
    """Extract all text from the PDF."""
    doc = fitz.open(str(pdf_path))
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages)


def clean_text(text: str) -> str:
    """Remove page headers/footers and normalize whitespace."""
    text = re.sub(r"Open Design Specification for \.dwg files \d+", "", text)
    text = re.sub(r"-- \d+ of \d+ --", "", text)
    text = re.sub(r"www\.opendesign\.com", "", text)
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.rstrip()
        cleaned.append(stripped)
    return "\n".join(cleaned)


def split_into_chapters(text: str) -> list[tuple[int, str, str]]:
    """Split text into chapters based on known chapter headings.

    Returns list of (chapter_num, title, content).
    The search skips the Table of Contents by starting after the last ToC-style
    entry (where numbers and titles are on separate lines with dot leaders).
    """
    toc_end_match = re.search(
        r"PROXY ENTITY GRAPHICS\s*\.+\s*\d+", text, re.IGNORECASE
    )
    search_start = toc_end_match.end() if toc_end_match else 0

    chapter_positions = []

    for num, title in TOP_LEVEL_CHAPTERS:
        title_prefix = re.escape(title.split("(")[0].strip())[:40]
        pattern = re.compile(
            rf"(?:^|\n){num}\s+{title_prefix}",
            re.IGNORECASE,
        )
        match = pattern.search(text, pos=search_start)
        if match:
            chapter_positions.append((match.start(), num, title))

    chapter_positions.sort(key=lambda x: x[0])

    chapters = []
    for i, (pos, num, title) in enumerate(chapter_positions):
        if i + 1 < len(chapter_positions):
            end = chapter_positions[i + 1][0]
        else:
            end = len(text)
        content = text[pos:end].strip()
        chapters.append((num, title, content))

    return chapters


def chapter_to_markdown(num: int, title: str, content: str) -> str:
    """Convert a chapter's content to clean markdown."""
    lines = [f"# Chapter {num}: {title}", ""]

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue

        subsection = re.match(r"^(\d+\.\d+(?:\.\d+)*)\s+(.+)$", stripped)
        if subsection:
            depth = subsection.group(1).count(".")
            prefix = "#" * (depth + 2)
            lines.append(f"{prefix} {subsection.group(1)} {subsection.group(2)}")
            continue

        lines.append(stripped)

    return "\n".join(lines)


@click.command()
@click.option(
    "--pdf",
    type=click.Path(exists=True, path_type=Path),
    default=Path("knowledge/raw/OpenDesign_Specification_for_.dwg_files.pdf"),
    help="Path to the DWG specification PDF.",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=Path("knowledge/chapters"),
    help="Directory to write markdown chapter files.",
)
def main(pdf: Path, output_dir: Path) -> None:
    """Extract DWG specification PDF into structured markdown chapters."""
    output_dir.mkdir(parents=True, exist_ok=True)

    click.echo(f"Extracting text from {pdf}...")
    raw_text = extract_full_text(pdf)

    click.echo("Cleaning text...")
    clean = clean_text(raw_text)

    full_path = output_dir / "full_specification.md"
    full_path.write_text(f"# OpenDesign Specification for .dwg files\n\n{clean}", encoding="utf-8")
    click.echo(f"  Wrote full specification: {full_path}")

    click.echo("Splitting into chapters...")
    chapters = split_into_chapters(clean)
    click.echo(f"  Found {len(chapters)} chapters")

    for num, title, content in chapters:
        md = chapter_to_markdown(num, title, content)
        safe_title = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")[:50]
        filename = f"ch{num:02d}_{safe_title}.md"
        filepath = output_dir / filename
        filepath.write_text(md, encoding="utf-8")
        click.echo(f"  Wrote: {filename}")

    click.echo(f"\nDone! Extracted {len(chapters)} chapters to {output_dir}")


if __name__ == "__main__":
    main()
