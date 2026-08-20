"""Domain MCP tool contracts for pytest — names, annotations, call results.

This is not protocol conformance. Do not wrap the official MCP conformance CLI.
"""

from .assert_mcp import (
    assert_call_equals,
    assert_non_readonly_tools_named,
    assert_subset_named,
    assert_tool_annotated_read_only,
    assert_tools_named,
    non_readonly_tool_names,
)

__version__ = "0.1.2"

__all__ = [
    "assert_call_equals",
    "assert_non_readonly_tools_named",
    "assert_subset_named",
    "assert_tool_annotated_read_only",
    "assert_tools_named",
    "non_readonly_tool_names",
]
