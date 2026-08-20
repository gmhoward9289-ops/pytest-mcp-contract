"""Minimal MCP server for the proof-stack example (no stdio)."""

from __future__ import annotations

from typing import Any, Dict

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

server = MCPServer(name="demo", title="Demo proof stack", version="0.0.1")

_READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    openWorldHint=False,
    idempotentHint=True,
)
_WRITE = ToolAnnotations(
    readOnlyHint=False,
    destructiveHint=False,
    openWorldHint=False,
    idempotentHint=False,
)


@server.tool(name="demo_status", annotations=_READ_ONLY)
async def demo_status() -> Dict[str, Any]:
    return {"ok": True}


@server.tool(name="demo_search", annotations=_READ_ONLY)
async def demo_search(query: str, limit: int = 5) -> Dict[str, Any]:
    return {"ok": True, "query": query, "limit": limit}


@server.tool(name="demo_enqueue", annotations=_WRITE)
async def demo_enqueue(task: str) -> Dict[str, Any]:
    return {"ok": True, "task": task}
