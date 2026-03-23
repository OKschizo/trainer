"""Tests for AutoCAD manual planning helpers."""

from autocad_mcp.planning import (
    build_feature_brief,
    build_workflow_outline,
    format_search_results,
)

SAMPLE_RESULTS = [
    {
        "source": "ch20_walls.md",
        "chapter": "Chapter 20: Walls",
        "section": "Drawing Walls",
        "page_start": 1147,
        "page_end": 1149,
        "text": "Use wall tools to create walls, then edit grips and styles.",
    },
    {
        "source": "ch20_walls.md",
        "chapter": "Chapter 20: Walls",
        "section": "Wall Styles",
        "page_start": 1282,
        "page_end": 1302,
        "text": "Wall styles define components, materials, and display properties.",
    },
]


def test_format_search_results_includes_labels():
    output = format_search_results(
        SAMPLE_RESULTS,
        heading="AutoCAD manual search results",
        empty_message="No results",
    )
    assert "AutoCAD manual search results" in output
    assert "Chapter 20: Walls -> Drawing Walls" in output
    assert "pages 1147-1149" in output


def test_build_feature_brief_separates_manual_and_inferred_content():
    output = build_feature_brief(
        feature_name="walls",
        browser_target="browser CAD app",
        results=SAMPLE_RESULTS,
    )
    assert "# Feature brief: walls" in output
    assert "## Manual-grounded requirements" in output
    assert "## Inferred browser-engineering tasks" in output
    assert "Wall Styles" in output


def test_build_workflow_outline_returns_checklist_and_evidence():
    output = build_workflow_outline("wall creation", SAMPLE_RESULTS)
    assert "# Workflow map: wall creation" in output
    assert "## Implementation checklist" in output
    assert "Drawing Walls" in output
