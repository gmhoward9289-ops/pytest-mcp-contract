"""Refresh tool input schema snapshots: python -m mcp_contract snapshot PATH."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from mcp_contract.session import list_tool_names


def _load_server(module: str):
    import importlib

    mod = importlib.import_module(module)
    server = getattr(mod, "server", None)
    if server is None:
        raise SystemExit(f"{module} has no server attribute")
    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MCP contract utilities")
    sub = parser.add_subparsers(dest="cmd", required=True)

    snap = sub.add_parser("snapshot", help="write tool input schemas JSON")
    snap.add_argument("path", type=Path, help="output JSON file")
    snap.add_argument(
        "--module",
        default="swamp_ops.server",
        help="module providing MCPServer (default: swamp_ops.server)",
    )
    snap.add_argument(
        "--tools",
        nargs="*",
        help="subset of tool names (default: all registered)",
    )

    args = parser.parse_args(argv)
    if args.cmd == "snapshot":
        from mcp_contract.schemas import snapshot_tool_input_schemas

        server = _load_server(args.module)
        schemas = snapshot_tool_input_schemas(server)
        if args.tools:
            keep = set(args.tools)
            schemas = {k: v for k, v in schemas.items() if k in keep}
        args.path.write_text(
            json.dumps(schemas, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"wrote {len(schemas)} schemas to {args.path}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
