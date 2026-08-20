"""Snapshot and compare MCP tool input JSON schemas from in-memory registration."""

from __future__ import annotations

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


def snapshot_tool_input_schemas(server: Any) -> dict[str, dict[str, Any]]:
    """All registered tool input schemas, sorted by tool name."""
    return {
        name: tool_input_schema(server, name)
        for name in sorted(list_tool_names(server))
    }


def _canonical(schema: dict[str, Any]) -> str:
    return json.dumps(schema, sort_keys=True, indent=2)


def assert_tool_input_schemas_match(
    server: Any,
    expected: dict[str, dict[str, Any]],
    *,
    tools: set[str] | None = None,
) -> None:
    """Fail when any pinned tool's input schema differs from the snapshot."""
    actual = snapshot_tool_input_schemas(server)
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
                f"{name}: schema drift\n"
                f"expected:\n{_canonical(expected[name])}\n"
                f"actual:\n{_canonical(actual[name])}"
            )
    if errors:
        raise AssertionError("\n---\n".join(errors))
