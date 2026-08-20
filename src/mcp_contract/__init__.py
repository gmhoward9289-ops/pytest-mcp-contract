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
from .schemas import (
    assert_tool_input_schemas_match,
    snapshot_tool_input_schemas,
    tool_input_schema,
)

__version__ = "0.1.3"

__all__ = [
    "assert_call_equals",
    "assert_non_readonly_tools_named",
    "assert_subset_named",
    "assert_tool_annotated_read_only",
    "assert_tool_input_schemas_match",
    "assert_tools_named",
    "non_readonly_tool_names",
    "snapshot_tool_input_schemas",
    "tool_input_schema",
]
