"""Registry + schema assertions for the demo MCP server."""

from __future__ import annotations

import json
from pathlib import Path

from mcp_contract.assert_mcp import (
    assert_non_readonly_tools_named,
    assert_non_readonly_tools_non_destructive,
    assert_tool_annotated_read_only,
    assert_tools_named,
    assert_tools_prefixed,
)
from mcp_contract.schemas import assert_tool_input_schemas_match, assert_tool_output_schemas_match
from mcp_contract.session import call_registered_tool, get_registered_tool, list_tool_names, tool_registry

DEMO_TOOLS = {"demo_status", "demo_search", "demo_enqueue"}
WRITE_TOOLS = {"demo_enqueue"}
SCHEMA_FIXTURE = Path(__file__).parent / "fixtures" / "mcp_tool_schemas.json"
OUTPUT_SCHEMA_FIXTURE = Path(__file__).parent / "fixtures" / "mcp_tool_output_schemas.json"


def test_demo_tool_names(mcp_server):
    names = list_tool_names(mcp_server)
    assert_tools_named(names, DEMO_TOOLS)
    assert_tools_prefixed(names, "demo_")


def test_write_tools_annotated(mcp_server):
    assert_non_readonly_tools_named(tool_registry(mcp_server), WRITE_TOOLS)
    assert_non_readonly_tools_non_destructive(tool_registry(mcp_server), WRITE_TOOLS)


def test_read_only_tools(mcp_server):
    for name in ("demo_status", "demo_search"):
        assert_tool_annotated_read_only(get_registered_tool(mcp_server, name))


def test_input_schemas(mcp_server):
    expected = json.loads(SCHEMA_FIXTURE.read_text(encoding="utf-8"))
    assert_tool_input_schemas_match(mcp_server, expected, tools=DEMO_TOOLS)


def test_output_schemas(mcp_server):
    expected = json.loads(OUTPUT_SCHEMA_FIXTURE.read_text(encoding="utf-8"))
    assert_tool_output_schemas_match(mcp_server, expected, tools=DEMO_TOOLS)


def test_demo_search_handler(mcp_server):
    result = call_registered_tool(
        mcp_server, "demo_search", query="setup", limit=3,
    )
    assert result == {"ok": True, "query": "setup", "limit": 3}
