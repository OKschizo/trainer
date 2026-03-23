"""Search engine for the AutoCAD manual vector store."""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "autocad_manual"
DEFAULT_DB_PATH = Path("knowledge/autocad_vectordb")
DEFAULT_MODEL = "all-MiniLM-L6-v2"


class AutoCADManualSearch:
    """Semantic search over the AutoCAD manual."""

    def __init__(
        self,
        db_path: Path = DEFAULT_DB_PATH,
        model: str = DEFAULT_MODEL,
    ):
        self._ef = SentenceTransformerEmbeddingFunction(model_name=model)
        self._client = chromadb.PersistentClient(path=str(db_path))
        self._collection = self._client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=self._ef,
        )

    @property
    def document_count(self) -> int:
        return self._collection.count()

    def search(
        self,
        query: str,
        n_results: int = 5,
        where_source: str | None = None,
        where_chapter: str | None = None,
    ) -> list[dict]:
        """Search the AutoCAD manual for relevant chunks."""
        filters: dict[str, str] = {}
        if where_source:
            filters["source"] = where_source
        if where_chapter:
            filters["chapter"] = where_chapter

        where = filters or None
        results = self._collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        output = []
        if results["documents"] and results["documents"][0]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                output.append(
                    {
                        "text": doc,
                        "source": meta.get("source", ""),
                        "chapter": meta.get("chapter", ""),
                        "section": meta.get("section", ""),
                        "page_start": meta.get("page_start", ""),
                        "page_end": meta.get("page_end", ""),
                        "distance": dist,
                    }
                )
        return output

    def list_sources(self) -> list[str]:
        """List all indexed source files."""
        results = self._collection.get(include=["metadatas"])
        return sorted({m.get("source", "") for m in results["metadatas"] if m})

    def list_chapters(self) -> list[str]:
        """List all indexed chapter titles."""
        results = self._collection.get(include=["metadatas"])
        return sorted({m.get("chapter", "") for m in results["metadatas"] if m})
