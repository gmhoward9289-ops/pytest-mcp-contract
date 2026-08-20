"""Domain MCP tool contracts for pytest — names, annotations, call results.

This is not protocol conformance. Do not wrap the official MCP conformance CLI.
"""

from .assert_mcp import (
    assert_call_equals,
    assert_non_readonly_tools_named,
    assert_non_readonly_tools_non_destructive,
    assert_subset_named,
    assert_tool_annotated_non_destructive,
    assert_tool_annotated_read_only,
    assert_tools_named,
    assert_tools_prefixed,
    non_readonly_tool_names,
)
from .schemas import (
    assert_tool_input_schemas_match,
    assert_tool_output_schemas_match,
    format_schema_drift,
    format_tool_input_schema_drift,
    format_tool_output_schema_drift,
    snapshot_tool_input_schemas,
    snapshot_tool_output_schemas,
    tool_input_schema,
    tool_output_schema,
)

__version__ = "0.1.6"

__all__ = [
    "assert_call_equals",
    "assert_non_readonly_tools_named",
    "assert_non_readonly_tools_non_destructive",
    "assert_subset_named",
    "assert_tool_annotated_non_destructive",
    "assert_tool_annotated_read_only",
    "assert_tool_input_schemas_match",
    "assert_tool_output_schemas_match",
    "assert_tools_named",
    "assert_tools_prefixed",
    "format_schema_drift",
    "format_tool_input_schema_drift",
    "format_tool_output_schema_drift",
    "non_readonly_tool_names",
    "snapshot_tool_input_schemas",
    "snapshot_tool_output_schemas",
    "tool_input_schema",
    "tool_output_schema",
]
