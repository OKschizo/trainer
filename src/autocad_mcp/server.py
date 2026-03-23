"""MCP server for AutoCAD manual-driven product design planning."""

from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from autocad_mcp.planning import (
    build_feature_brief,
    build_workflow_outline,
    format_search_results,
)
from autocad_mcp.search import AutoCADManualSearch

DEFAULT_CHAPTERS_DIR = Path(
    os.getenv("AUTOCAD_MCP_CHAPTERS_DIR", "knowledge/autocad_chapters")
)

mcp = FastMCP(
    "AutoCAD Product Design Expert",
    instructions=(
        "You are an expert product-design copilot for building an open-source, "
        "browser-based AutoCAD-like application. Use the provided tools to retrieve "
        "relevant sections from the indexed AutoCAD manual, then produce concrete "
        "implementation guidance: workflows, UI affordances, domain objects, "
        "constraints, and scoped milestones. When making recommendations, separate "
        "manual-grounded requirements from inferred engineering advice."
    ),
)

_search: AutoCADManualSearch | None = None


def _get_search() -> AutoCADManualSearch:
    global _search
    if _search is None:
        _search = AutoCADManualSearch()
    return _search


@mcp.tool()
def search_autocad_manual(query: str, n_results: int = 6) -> str:
    """Search the indexed AutoCAD manual for feature, UI, or workflow details."""
    search = _get_search()
    n_results = max(1, min(20, n_results))
    return format_search_results(
        search.search(query, n_results=n_results),
        heading="AutoCAD manual search results",
        empty_message="No relevant passages found. Try a narrower feature or workflow query.",
    )


@mcp.tool()
def list_autocad_sources() -> str:
    """List indexed chapter files for the AutoCAD manual knowledge base."""
    search = _get_search()
    sources = search.list_sources()
    count = search.document_count

    parts = [
        f"AutoCAD Manual Index ({count} chunks across {len(sources)} files)\n",
        "Available sources:",
    ]
    for source in sources:
        parts.append(f"  - {source}")
    return "\n".join(parts)


@mcp.tool()
def get_autocad_chapter(chapter_slug: str) -> str:
    """Return a full extracted AutoCAD chapter by filename stem or prefix."""
    if not DEFAULT_CHAPTERS_DIR.exists():
        return "Error: chapter directory not found. Run 'autocad-extract' first."

    normalized = chapter_slug.strip().lower().replace(" ", "_")
    matches = sorted(
        path
        for path in DEFAULT_CHAPTERS_DIR.glob("*.md")
        if path.stem.lower().startswith(normalized)
    )
    if not matches:
        return f"No chapter found matching '{chapter_slug}'."
    return matches[0].read_text(encoding="utf-8")


@mcp.tool()
def plan_autocad_feature(feature_name: str, browser_target: str = "web browser") -> str:
    """Generate an implementation brief for a browser-based AutoCAD feature."""
    search = _get_search()
    queries = [
        f"{feature_name} workflow create edit properties commands",
        f"{feature_name} style display settings constraints",
        f"{feature_name} user interface palette ribbon grips command line",
    ]

    merged_results: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for query in queries:
        for result in search.search(query, n_results=4):
            key = (result["source"], result["text"])
            if key in seen:
                continue
            seen.add(key)
            merged_results.append(result)

    if not merged_results:
        return f"No manual guidance found for feature '{feature_name}'."

    return build_feature_brief(
        feature_name=feature_name,
        browser_target=browser_target,
        results=merged_results,
    )


@mcp.tool()
def map_autocad_workflow(workflow_name: str) -> str:
    """Build a stepwise workflow map from the AutoCAD manual."""
    search = _get_search()
    results = search.search(
        f"{workflow_name} workflow steps prerequisites commands properties",
        n_results=8,
    )
    if not results:
        return f"No workflow guidance found for '{workflow_name}'."
    return build_workflow_outline(workflow_name=workflow_name, results=results)


def main() -> None:
    """Run the AutoCAD MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
