"""Search engine for the DWG specification vector store."""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "dwg_specification"
DEFAULT_DB_PATH = Path("knowledge/vectordb")
DEFAULT_MODEL = "all-MiniLM-L6-v2"


class DwgSpecSearch:
    """Semantic search over the DWG specification."""

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
    ) -> list[dict]:
        """Search the specification for relevant chunks.

        Args:
            query: Natural language query about the DWG format.
            n_results: Number of results to return.
            where_source: Optional filter to a specific chapter source file.

        Returns:
            List of dicts with keys: text, source, section, distance.
        """
        where = None
        if where_source:
            where = {"source": where_source}

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
                        "section": meta.get("section", ""),
                        "distance": dist,
                    }
                )
        return output

    def list_sources(self) -> list[str]:
        """List all indexed source files (chapters)."""
        results = self._collection.get(include=["metadatas"])
        sources = sorted({m.get("source", "") for m in results["metadatas"] if m})
        return sources
