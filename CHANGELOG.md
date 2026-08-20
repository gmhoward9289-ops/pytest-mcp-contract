# Changelog

## 0.1.3

- `assert_tool_input_schemas_match`, `snapshot_tool_input_schemas`, `tool_input_schema`
- `python -m mcp_contract snapshot` CLI to refresh schema JSON files

## 0.1.2

- `call_registered_tool` awaits async MCP handlers via `asyncio.run`
- `acall_registered_tool` for explicit async pytest tests

## 0.1.1

- Initial PyPI release: tool name set assertions, read-only annotation checks, in-memory handler calls
