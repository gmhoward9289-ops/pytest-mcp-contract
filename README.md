# pytest-mcp-contract

Pytest helpers for **domain MCP tool contracts**: registered names, annotations, and in-memory handler calls.

This is **not** protocol conformance. It does not wrap `npx @modelcontextprotocol/conformance`, does not ship security payloads, and does not run an LLM in CI.

## Install

```bash
pip install -e ".[mcp]"
```

The `mcp` extra pins the MCP Python SDK the same way swamp-ops does today: `mcp[cli]>=2.0.0` (SDK 2.x `MCPServer`).

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

Calls go through the registered `Tool.fn` handler, not `mcp.Client`. v1 is in-memory only.

## See also

- [MCP Python SDK testing](https://github.com/modelcontextprotocol/python-sdk)
- FastMCP client/session docs in that SDK

Those cover protocol and transport. This plugin asserts *your* tool set.

## License

Apache-2.0
