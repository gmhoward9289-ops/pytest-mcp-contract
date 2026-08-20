# pytest-mcp-contract

[![Discussions](https://img.shields.io/github/discussions/gmhoward9289-ops/pytest-mcp-contract)](https://github.com/gmhoward9289-ops/pytest-mcp-contract/discussions)

Pytest helpers for **domain MCP tool contracts**: registered names, annotations, input schemas, and in-memory handler calls.

This is **not** protocol conformance. It does not wrap `npx @modelcontextprotocol/conformance`, does not ship security payloads, and does not run an LLM in CI.

## Install

```bash
pip install pytest-mcp-contract
# or pinned tag:
pip install git+https://github.com/gmhoward9289-ops/pytest-mcp-contract@v0.1.6
```

For in-memory registry access against the MCP Python SDK:

```bash
pip install "pytest-mcp-contract[mcp]"
```

The `mcp` extra pins the MCP Python SDK the same way swamp-ops does today: `mcp[cli]>=2.0.0` (SDK 2.x `MCPServer`).

Develop from a git checkout:

```bash
pip install -e ".[mcp]"
```

## Usage

Override the `mcp_server` fixture with your server object. The plugin lists names from the in-memory registry (no stdio subprocess).

```python
import pytest
from mcp_contract.assert_mcp import assert_tools_named
from mcp_contract.session import list_tool_names

@pytest.fixture
def mcp_server():
    from swamp_ops.server import server
    return server

def test_tool_names(mcp_server):
    assert_tools_named(list_tool_names(mcp_server), {"swamp_estate_status", ...})
```

`list_tool_names` reads `MCPServer._tool_manager._tools` (or `tool_manager._tools`). That is the same private registry swamp-ops already inspects. If the shape is unknown, the helper **fails** instead of skipping — registry drift is what this plugin is for.

Pin write tools and their safety annotations:

```python
from mcp_contract.assert_mcp import (
    assert_non_readonly_tools_non_destructive,
    assert_tools_prefixed,
)
from mcp_contract.session import list_tool_names, tool_registry

def test_write_tools(mcp_server):
    names = list_tool_names(mcp_server)
    assert_tools_prefixed(names, "swamp_")
    assert_non_readonly_tools_non_destructive(
        tool_registry(mcp_server),
        {"swamp_enqueue_job", "swamp_post_discussion", ...},
    )
```

Calls go through the registered `Tool.fn` handler, not `mcp.Client`. v1 is in-memory only. Async handlers are supported: `call_registered_tool` uses `asyncio.run`; use `acall_registered_tool` inside async tests.

### Input schema snapshots

Pin tool input JSON schemas and fail CI on accidental drift:

```python
import json
from pathlib import Path
from mcp_contract.schemas import assert_tool_input_schemas_match

@pytest.fixture
def mcp_server():
    from swamp_ops.server import server
    return server

def test_schemas(mcp_server):
    expected = json.loads(Path("tests/fixtures/mcp_schemas.json").read_text())
    assert_tool_input_schemas_match(mcp_server, expected, tools=set(expected))
```

Refresh a snapshot from a live server module:

```text
python -m mcp_contract snapshot tests/fixtures/mcp_schemas.json --module swamp_ops.server
```

On drift, failures show dotted field paths (`properties.repo.type`) and a unified diff — not two full JSON blobs.

### Output schema snapshots

Pin structured handler output JSON schemas the same way (MCP SDK `Tool.output_schema`):

```python
from mcp_contract.schemas import assert_tool_output_schemas_match

def test_output_schemas(mcp_server):
    expected = json.loads(Path("tests/fixtures/mcp_output_schemas.json").read_text())
    assert_tool_output_schemas_match(mcp_server, expected, tools=set(expected))
```

Refresh:

```text
python -m mcp_contract snapshot tests/fixtures/mcp_output_schemas.json --output --module swamp_ops.server
```

### Publish health

After each tag release, CI runs `packaging/publish-doctor.sh` (also daily) to verify PyPI serves the same version as `src/mcp_contract/__init__.py`. Local check:

```bash
bash packaging/publish-doctor.sh
```

## Proof stack (pair with pytest-session-trace)

| Plugin | Asserts |
| --- | --- |
| **pytest-mcp-contract** (this repo) | MCP server registers the right tool names, annotations, input schemas, and handlers |
| [pytest-session-trace](https://github.com/gmhoward9289-ops/pytest-session-trace) | A saved agent session (JSONL) actually called those tools in order |

Use both in the same repo: registry correctness **and** agent behavior — still no LLM in CI. swamp-ops dogfoods the pair in `test_mcp_contract.py`, `test_session_trace.py`, and `docs/SESSION_TRACE.md`.

Public starter (no private ops repo): [`examples/proof_stack/`](examples/proof_stack/) — synthetic JSONL, pinned schemas, and both test files in one folder.

## See also

- [pytest-session-trace](https://github.com/gmhoward9289-ops/pytest-session-trace) — assert what an agent *called* in a saved JSONL session (pairs with this plugin: registry vs behavior)
- [MCP Python SDK testing](https://github.com/modelcontextprotocol/python-sdk)
- FastMCP client/session docs in that SDK

Those cover protocol and transport. This plugin asserts *your* tool set.

## License

Apache-2.0
