"""Plugin fixtures: tests supply mcp_server; the plugin lists names."""

from __future__ import annotations

import pytest

import fake_server


@pytest.fixture
def mcp_server():
    return fake_server.server


def test_mcp_tool_names_from_plugin(mcp_tool_names):
    assert mcp_tool_names == {"echo"}
