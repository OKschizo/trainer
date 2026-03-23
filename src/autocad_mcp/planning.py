"""Planning helpers for building a browser-based AutoCAD alternative."""

from __future__ import annotations

from collections import Counter


def _result_label(result: dict) -> str:
    page_start = result.get("page_start")
    page_end = result.get("page_end")
    if page_start and page_end and page_start != page_end:
        page_label = f"pages {page_start}-{page_end}"
    elif page_start:
        page_label = f"page {page_start}"
    else:
        page_label = "page unknown"
    return (
        f"{result.get('chapter', 'Unknown chapter')} -> "
        f"{result.get('section', 'Unknown section')} "
        f"({result.get('source', 'unknown source')}, {page_label})"
    )


def format_search_results(
    results: list[dict],
    *,
    heading: str,
    empty_message: str,
) -> str:
    """Format semantic search results for MCP responses."""
    if not results:
        return empty_message

    parts = [heading, ""]
    for index, result in enumerate(results, start=1):
        parts.append(f"--- Result {index}: {_result_label(result)} ---")
        parts.append(result["text"])
        parts.append("")
    return "\n".join(parts).strip()


def build_feature_brief(
    feature_name: str,
    browser_target: str,
    results: list[dict],
) -> str:
    """Turn retrieved guide passages into a manual-grounded implementation brief."""
    if not results:
        return (
            f"No guide passages found for '{feature_name}'. Try a broader feature "
            "name or search for adjacent workflows first."
        )

    section_counts = Counter(result["section"] for result in results if result.get("section"))
    top_sections = [section for section, _ in section_counts.most_common(6)]
    primary_sources = sorted({result["source"] for result in results if result.get("source")})[:6]

    parts = [
        f"# Feature brief: {feature_name}",
        "",
        "## Goal",
        (
            f"Implement a {browser_target} version of '{feature_name}' using the "
            "manual as the source of truth for workflows, editable properties, "
            "and supporting UI surfaces."
        ),
        "",
        "## Manual-grounded focus areas",
    ]

    if top_sections:
        for section in top_sections:
            parts.append(f"- {section}")
    else:
        parts.append("- Review the retrieved passages to identify the core workflows.")

    parts.extend(
        [
            "",
            "## Manual-grounded requirements",
            "- Provide an obvious entry point such as a tool, command, ribbon control, or palette action.",
            "- Support the creation workflow described in the guide, including intermediate prompts or placement states.",
            "- Expose the editable properties, style options, and overrides mentioned in the retrieved sections.",
            "- Preserve the feature in the document model so it survives save, reload, and copy operations.",
            "- Support follow-up editing flows such as grips, style reassignment, or property changes when documented.",
            "",
            "## Inferred browser-engineering tasks",
            "- Map the feature to a domain entity and persistent schema in your browser CAD document model.",
            "- Implement canvas interactions for placement, snapping, selection, hover, and drag handles.",
            "- Add a property inspector or contextual side panel for post-creation edits.",
            "- Render geometry and annotations consistently across normal, selected, and editing states.",
            "- Add automated tests for creation, mutation, serialization, and viewport rendering.",
            "",
            "## Suggested build order",
            "1. Build the domain model and serialization contract.",
            "2. Implement the primary creation command and basic rendering.",
            "3. Add property editing, style support, and documented overrides.",
            "4. Add secondary editing workflows such as grips, anchors, or conversion tools.",
            "5. Add regression tests based on the workflow steps captured below.",
            "",
            "## Primary guide sources",
        ]
    )
    for source in primary_sources:
        parts.append(f"- {source}")

    parts.extend(["", "## Supporting passages"])
    for index, result in enumerate(results, start=1):
        parts.append(f"### Passage {index}: {_result_label(result)}")
        parts.append(result["text"])
        parts.append("")

    return "\n".join(parts).strip()


def build_workflow_outline(workflow_name: str, results: list[dict]) -> str:
    """Summarize user workflows from retrieved manual passages."""
    if not results:
        return f"No workflow passages found for '{workflow_name}'."

    parts = [
        f"# Workflow map: {workflow_name}",
        "",
        "## Implementation checklist",
        "- Identify the entry command, toolbar action, palette action, or shortcut.",
        "- Capture the temporary state transitions that occur while the command is active.",
        "- Model the prompts, options, and confirmations shown to the user.",
        "- Apply the resulting geometry or object mutations with undo-friendly checkpoints.",
        "- Support the follow-up editing behaviors referenced in the same workflow area.",
        "",
        "## Retrieved workflow evidence",
    ]

    for index, result in enumerate(results, start=1):
        parts.append(f"{index}. {_result_label(result)}")
        parts.append(result["text"])
        parts.append("")

    return "\n".join(parts).strip()
