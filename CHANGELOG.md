# Changelog

## 0.1.5

- `format_tool_input_schema_drift` — field-level change paths plus unified diff on schema mismatch
- `publish-doctor.sh` reads `__version__` from `src/mcp_contract/__init__.py` (Windows Git Bash friendly)

## 0.1.4

- `assert_tools_prefixed` — pin a namespace prefix on every tool name
- `assert_tool_annotated_non_destructive`, `assert_non_readonly_tools_non_destructive` — write tools must not be marked destructive
- `release.yml` attaches wheel/sdist to GitHub Releases on tag

## 0.1.3

- `assert_tool_input_schemas_match`, `snapshot_tool_input_schemas`, `tool_input_schema`
- `python -m mcp_contract snapshot` CLI to refresh schema JSON files

## 0.1.2

- `call_registered_tool` awaits async MCP handlers via `asyncio.run`
- `acall_registered_tool` for explicit async pytest tests

## 0.1.1

- Initial PyPI release: tool name set assertions, read-only annotation checks, in-memory handler calls
