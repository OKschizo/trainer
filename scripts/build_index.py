"""Build a ChromaDB vector index from the extracted DWG specification chapters."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

import chromadb
import click
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

DEFAULT_CHUNK_SIZE = 1500
DEFAULT_CHUNK_OVERLAP = 200
COLLECTION_NAME = "dwg_specification"
DB_PATH = "knowledge/vectordb"


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """Split text into overlapping chunks, preserving section context."""
    chunks = []
    current_section = ""
    chunk_index = 0

    lines = text.split("\n")
    current_chunk_lines: list[str] = []
    current_length = 0

    for line in lines:
        heading_match = re.match(r"^(#{1,5})\s+(.+)$", line)
        if heading_match:
            current_section = heading_match.group(2)

        line_len = len(line) + 1
        if current_length + line_len > chunk_size and current_chunk_lines:
            chunk_text_str = "\n".join(current_chunk_lines)
            chunk_id = hashlib.sha256(
                f"{source}:{chunk_index}:{chunk_text_str[:100]}".encode()
            ).hexdigest()[:16]
            chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text_str,
                    "source": source,
                    "section": current_section,
                }
            )
            chunk_index += 1

            overlap_lines: list[str] = []
            overlap_len = 0
            for prev_line in reversed(current_chunk_lines):
                if overlap_len + len(prev_line) + 1 > chunk_overlap:
                    break
                overlap_lines.insert(0, prev_line)
                overlap_len += len(prev_line) + 1

            current_chunk_lines = overlap_lines
            current_length = overlap_len

        current_chunk_lines.append(line)
        current_length += line_len

    if current_chunk_lines:
        chunk_text_str = "\n".join(current_chunk_lines)
        chunk_id = hashlib.sha256(
            f"{source}:{chunk_index}:{chunk_text_str[:100]}".encode()
        ).hexdigest()[:16]
        chunks.append(
            {
                "id": chunk_id,
                "text": chunk_text_str,
                "source": source,
                "section": current_section,
            }
        )

    return chunks


@click.command()
@click.option(
    "--chapters-dir",
    type=click.Path(exists=True, path_type=Path),
    default=Path("knowledge/chapters"),
    help="Directory containing markdown chapter files.",
)
@click.option(
    "--db-path",
    type=click.Path(path_type=Path),
    default=Path(DB_PATH),
    help="Path for the ChromaDB persistent storage.",
)
@click.option(
    "--chunk-size",
    type=int,
    default=DEFAULT_CHUNK_SIZE,
    help="Maximum chunk size in characters.",
)
@click.option(
    "--model",
    type=str,
    default="all-MiniLM-L6-v2",
    help="Sentence transformer model for embeddings.",
)
def main(chapters_dir: Path, db_path: Path, chunk_size: int, model: str) -> None:
    """Build vector index from extracted DWG specification chapters."""
    db_path.mkdir(parents=True, exist_ok=True)

    click.echo(f"Using embedding model: {model}")
    ef = SentenceTransformerEmbeddingFunction(model_name=model)

    client = chromadb.PersistentClient(path=str(db_path))

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        click.echo(f"Deleted existing collection '{COLLECTION_NAME}'")

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"description": "OpenDesign Specification for .dwg files v5.4.1"},
    )

    md_files = sorted(chapters_dir.glob("*.md"))
    click.echo(f"Found {len(md_files)} markdown files to index")

    all_chunks: list[dict] = []
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        chunks = chunk_text(text, source=md_file.name, chunk_size=chunk_size)
        all_chunks.extend(chunks)
        click.echo(f"  {md_file.name}: {len(chunks)} chunks")

    click.echo(f"\nTotal chunks: {len(all_chunks)}")

    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i : i + batch_size]
        collection.add(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            metadatas=[{"source": c["source"], "section": c["section"]} for c in batch],
        )
        total_batches = (len(all_chunks) + batch_size - 1) // batch_size
        click.echo(f"  Indexed batch {i // batch_size + 1}/{total_batches}")

    click.echo(f"\nDone! Indexed {len(all_chunks)} chunks into {db_path}")
    click.echo(f"Collection '{COLLECTION_NAME}' has {collection.count()} documents")


if __name__ == "__main__":
    main()
