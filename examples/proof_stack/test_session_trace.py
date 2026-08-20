"""Saved session assertions for the demo agent flow."""

from __future__ import annotations

from pathlib import Path

from henhouse import load_tool_calls
from session_trace.assert_tools import (
    assert_no_tool,
    assert_tool_called,
    assert_tool_input_contains,
    assert_tool_order,
)

FIXTURE = Path(__file__).parent / "fixtures" / "agent_check.jsonl"


def test_agent_check_flow(session_trace):
    assert_tool_order(session_trace, ["demo_status", "demo_search"])
    assert_tool_called(session_trace, "demo_status")
    assert_tool_called(session_trace, "demo_search")
    assert_tool_input_contains(session_trace, "demo_search", "query", "setup")
    assert_tool_input_contains(session_trace, "demo_search", "limit", "3")
    assert_no_tool(session_trace, "demo_enqueue")


def test_fixture_parses_with_henhouse():
    calls = load_tool_calls(FIXTURE)
    assert [c.name for c in calls] == ["demo_status", "demo_search"]
