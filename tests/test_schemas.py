"""Schema snapshot helpers."""

from __future__ import annotations

import pytest

from mcp_contract.schemas import (
    assert_tool_input_schemas_match,
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
    with pytest.raises(AssertionError, match="schema drift"):
        assert_tool_input_schemas_match(fake_server.server, expected, tools={"echo"})
