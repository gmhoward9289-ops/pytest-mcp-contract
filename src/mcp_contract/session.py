"""In-memory access to SDK 2.x MCPServer tool registration.

# Call path: registered handler (Tool.fn), not mcp.Client.
# A full in-memory Client session against MCPServer is out of v1 scope
# (no stdio subprocess; Windows signal/pid issues). Handler invocation
# proves the decorator bound a callable. Unknown registry shape fails
# loud — noticing that drift is this plugin's job.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any

_SHAPE_MSG = (
    "MCPServer tool registry shape not recognised: expected "
    "_tool_manager._tools or tool_manager._tools"
)


def tool_registry(server: Any) -> dict[str, Any]:
    manager = getattr(server, "_tool_manager", None) or getattr(server, "tool_manager", None)
    if manager is None or not hasattr(manager, "_tools"):
        raise RuntimeError(_SHAPE_MSG)
    tools = manager._tools
    if not isinstance(tools, dict):
        raise RuntimeError(_SHAPE_MSG)
    return tools


def list_tool_names(server: Any) -> set[str]:
    """Return registered tool names from MCPServer's in-memory registry."""
    return set(tool_registry(server))


def get_registered_tool(server: Any, name: str) -> Any:
    tools = tool_registry(server)
    try:
        return tools[name]
    except KeyError as exc:
        raise KeyError(f"tool {name!r} not registered") from exc


def call_registered_tool(server: Any, name: str, **kwargs: Any) -> Any:
    """Invoke a registered Tool.fn handler (sync or async).

    Async handlers are awaited via ``asyncio.run`` — fine for ordinary pytest
    tests. From inside a running event loop, use ``acall_registered_tool``.
    """
    tool = get_registered_tool(server, name)
    fn = getattr(tool, "fn", None)
    if fn is None or not callable(fn):
        raise RuntimeError(f"no callable handler (Tool.fn) on registered tool {name!r}")
    result = fn(**kwargs)
    if inspect.isawaitable(result):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(result)
        raise RuntimeError(
            f"tool {name!r} handler is async and an event loop is already running; "
            "use acall_registered_tool in async tests"
        )
    return result


async def acall_registered_tool(server: Any, name: str, **kwargs: Any) -> Any:
    """Await a registered Tool.fn handler (sync or async)."""
    tool = get_registered_tool(server, name)
    fn = getattr(tool, "fn", None)
    if fn is None or not callable(fn):
        raise RuntimeError(f"no callable handler (Tool.fn) on registered tool {name!r}")
    result = fn(**kwargs)
    if inspect.isawaitable(result):
        return await result
    return result
