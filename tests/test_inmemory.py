"""In-memory list/call against SDK 2.x MCPServer (no stdio)."""

from __future__ import annotations

import pytest

from mcp_contract.assert_mcp import assert_call_equals, assert_tool_annotated_read_only
from mcp_contract.session import call_registered_tool, list_tool_names

import fake_server


def test_list_tool_names_echo():
    assert list_tool_names(fake_server.server) == {"echo"}


def test_echo_handler_roundtrip():
    assert_call_equals(call_registered_tool(fake_server.server, "echo", text="ping"), "ping")


def test_echo_is_read_only():
    from mcp_contract.session import get_registered_tool

    assert_tool_annotated_read_only(get_registered_tool(fake_server.server, "echo"))


def test_unknown_registry_shape_fails():
    with pytest.raises(RuntimeError, match="registry shape"):
        list_tool_names(object())
