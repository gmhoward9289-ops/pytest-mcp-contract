# Proof stack example

Minimal, public, copy-pasteable example of the three-plugin stack:

| Package | What it proves |
| --- | --- |
| [pytest-mcp-contract](https://github.com/gmhoward9289-ops/pytest-mcp-contract) | Your MCP server registers the right tool names, annotations, input schemas, and handlers |
| [pytest-session-trace](https://github.com/gmhoward9289-ops/pytest-session-trace) | A saved agent session (JSONL) actually called those tools in order |
| [henhouse](https://github.com/gmhoward9289-ops/henhouse) | The JSONL parses into typed tool calls (parser drift fails before assertions) |

No LLM in CI. No network. No private ops repo required.

## Run it

From this directory:

```bash
pip install -r requirements.txt
pytest -q
```

Develop from sibling clones under `dev/` instead:

```bash
pip install -e ../../
pip install -e ../../../henhouse
pip install -e ../../../pytest-session-trace
pytest -q
```

## Layout

| File | Role |
| --- | --- |
| `demo_server.py` | Tiny in-memory `MCPServer` with three `demo_*` tools |
| `fixtures/agent_check.jsonl` | Synthetic session: `demo_status` then `demo_search` |
| `fixtures/mcp_tool_schemas.json` | Pinned input schemas (refresh with snapshot command below) |
| `fixtures/mcp_tool_output_schemas.json` | Pinned output schemas (`snapshot --output`) |
| `test_mcp_contract.py` | Registry, annotation, schema, and handler round-trip tests |
| `test_session_trace.py` | Session order/input assertions + henhouse parse check |

## Refresh the schema snapshot

After intentional handler signature changes:

```bash
python -m mcp_contract snapshot fixtures/mcp_tool_schemas.json --module demo_server
python -m mcp_contract snapshot fixtures/mcp_tool_output_schemas.json --output --module demo_server
```

## Record your own session

1. Run an agent session against your MCP server with tools enabled.
2. Redact secrets and home paths from the JSONL.
3. Point pytest at it: `pytest --session-trace path/to/session.jsonl`
4. Or codegen a starter test: `python -m session_trace path/to/session.jsonl > test_session.py`

See [pytest-session-trace Show and tell](https://github.com/gmhoward9289-ops/pytest-session-trace/discussions/categories/show-and-tell) for real-world patterns.
