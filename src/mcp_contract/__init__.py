"""Domain MCP tool contracts for pytest — names, annotations, call results.

This is not protocol conformance. Do not wrap the official MCP conformance CLI.
"""

from .assert_mcp import (
    assert_call_equals,
    assert_subset_named,
    assert_tool_annotated_read_only,
    assert_tools_named,
)

__version__ = "0.1.0"

__all__ = [
    "assert_call_equals",
    "assert_subset_named",
    "assert_tool_annotated_read_only",
    "assert_tools_named",
]
