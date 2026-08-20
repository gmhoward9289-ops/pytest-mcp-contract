"""Schema snapshot helpers."""

from __future__ import annotations

import pytest

from mcp_contract.schemas import (
    assert_tool_input_schemas_match,
    format_tool_input_schema_drift,
    snapshot_tool_input_schemas,
    tool_input_schema,
)

import fake_server


def test_tool_input_schema_echo():
    schema = tool_input_schema(fake_server.server, "echo")
    assert schema["properties"]["text"]["type"] == "string"


def test_snapshot_sorted_keys():
    snap = snapshot_tool_input_schemas(fake_server.server)
    assert list(snap) == sorted(snap)


def test_assert_schemas_match_passes():
    expected = snapshot_tool_input_schemas(fake_server.server)
    assert_tool_input_schemas_match(fake_server.server, expected)


def test_assert_schemas_detects_drift():
    expected = snapshot_tool_input_schemas(fake_server.server)
    expected["echo"] = {"type": "object", "properties": {}}
    with pytest.raises(AssertionError, match="schema drift") as exc:
        assert_tool_input_schemas_match(fake_server.server, expected, tools={"echo"})
    msg = str(exc.value)
    assert "changes:" in msg
    assert "@@" in msg  # unified diff hunk header


def test_format_tool_input_schema_drift_lists_paths():
    expected = {"type": "object", "properties": {"text": {"type": "string"}}}
    actual = {"type": "object", "properties": {"text": {"type": "integer"}}}
    report = format_tool_input_schema_drift(expected, actual)
    assert "properties.text.type" in report
    assert "--- expected" in report
    assert "+++ actual" in report
