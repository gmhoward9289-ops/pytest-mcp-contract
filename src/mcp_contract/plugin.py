"""pytest plugin: domain MCP contracts, not protocol conformance.

Provides ``mcp_tool_names`` when the test module supplies ``mcp_server``.
This plugin does not import any application (swamp-ops, etc.).
"""

from __future__ import annotations

import pytest


@pytest.fixture
def mcp_tool_names(mcp_server):
    from mcp_contract.session import list_tool_names

    return list_tool_names(mcp_server)
