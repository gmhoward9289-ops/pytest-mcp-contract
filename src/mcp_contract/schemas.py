"""Snapshot and compare MCP tool input/output JSON schemas from in-memory registration."""

from __future__ import annotations

import difflib
import json
from typing import Any

from mcp_contract.session import get_registered_tool, list_tool_names


def tool_input_schema(server: Any, name: str) -> dict[str, Any]:
    """Input parameters JSON schema for one registered tool."""
    tool = get_registered_tool(server, name)
    params = tool.parameters
    if isinstance(params, dict):
        return params
    raise TypeError(f"tool {name!r} parameters is not a dict: {type(params)!r}")


def tool_output_schema(server: Any, name: str) -> dict[str, Any]:
    """Structured output JSON schema for one registered tool."""
    tool = get_registered_tool(server, name)
    schema = tool.output_schema
    if schema is None:
        raise TypeError(f"tool {name!r} has no output_schema")
    if isinstance(schema, dict):
        return schema
    raise TypeError(f"tool {name!r} output_schema is not a dict: {type(schema)!r}")


def snapshot_tool_input_schemas(server: Any) -> dict[str, dict[str, Any]]:
    """All registered tool input schemas, sorted by tool name."""
    return {
        name: tool_input_schema(server, name)
        for name in sorted(list_tool_names(server))
    }


def snapshot_tool_output_schemas(server: Any) -> dict[str, dict[str, Any]]:
    """All registered tool output schemas, sorted by tool name."""
    return {
        name: tool_output_schema(server, name)
        for name in sorted(list_tool_names(server))
    }


def _canonical(schema: dict[str, Any]) -> str:
    return json.dumps(schema, sort_keys=True, indent=2)


def _field_changes(expected: Any, actual: Any, path: str = "$") -> list[str]:
    """Return dotted paths where ``actual`` differs from ``expected``."""
    if expected == actual:
        return []
    if isinstance(expected, dict) and isinstance(actual, dict):
        lines: list[str] = []
        for key in sorted(set(expected) | set(actual)):
            sub = f"{path}.{key}" if path != "$" else key
            if key not in expected:
                lines.append(f"+ {sub}")
            elif key not in actual:
                lines.append(f"- {sub}")
            else:
                lines.extend(_field_changes(expected[key], actual[key], sub))
        return lines
    if isinstance(expected, list) and isinstance(actual, list):
        if expected != actual:
            return [f"~ {path}: list changed"]
        return []
    return [f"~ {path}: {actual!r} (expected {expected!r})"]


def format_schema_drift(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> str:
    """Human-readable field summary plus unified diff for schema drift."""
    changes = _field_changes(expected, actual)
    diff = difflib.unified_diff(
        _canonical(expected).splitlines(),
        _canonical(actual).splitlines(),
        fromfile="expected",
        tofile="actual",
        lineterm="",
    )
    parts: list[str] = []
    if changes:
        parts.append("changes:\n  " + "\n  ".join(changes))
    else:
        parts.append("changes: (structural mismatch without path detail)")
    parts.append("")
    parts.extend(diff)
    return "\n".join(parts).rstrip()


def format_tool_input_schema_drift(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> str:
    """Backward-compatible alias for :func:`format_schema_drift`."""
    return format_schema_drift(expected, actual)


def format_tool_output_schema_drift(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> str:
    """Alias for output schema drift reporting."""
    return format_schema_drift(expected, actual)


def _assert_tool_schemas_match(
    server: Any,
    expected: dict[str, dict[str, Any]],
    *,
    tools: set[str] | None,
    snapshot_fn,
    drift_label: str,
) -> None:
    actual = snapshot_fn(server)
    want_names = sorted(tools if tools is not None else expected.keys())
    missing = set(want_names) - set(actual)
    assert not missing, f"tools not registered: {sorted(missing)}"

    errors: list[str] = []
    for name in want_names:
        if name not in expected:
            errors.append(f"{name}: missing from expected snapshot")
            continue
        if _canonical(actual[name]) != _canonical(expected[name]):
            errors.append(
                f"{name}: {drift_label}\n"
                f"{format_schema_drift(expected[name], actual[name])}"
            )
    if errors:
        raise AssertionError("\n---\n".join(errors))


def assert_tool_input_schemas_match(
    server: Any,
    expected: dict[str, dict[str, Any]],
    *,
    tools: set[str] | None = None,
) -> None:
    """Fail when any pinned tool's input schema differs from the snapshot."""
    _assert_tool_schemas_match(
        server,
        expected,
        tools=tools,
        snapshot_fn=snapshot_tool_input_schemas,
        drift_label="input schema drift",
    )


def assert_tool_output_schemas_match(
    server: Any,
    expected: dict[str, dict[str, Any]],
    *,
    tools: set[str] | None = None,
) -> None:
    """Fail when any pinned tool's output schema differs from the snapshot."""
    _assert_tool_schemas_match(
        server,
        expected,
        tools=tools,
        snapshot_fn=snapshot_tool_output_schemas,
        drift_label="output schema drift",
    )
