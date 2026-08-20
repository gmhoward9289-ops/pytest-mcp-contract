from mcp.server import MCPServer
from mcp.types import ToolAnnotations

server = MCPServer(name="fake", title="Fake", version="0.0.1")


@server.tool(
    name="echo",
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        openWorldHint=False,
        idempotentHint=True,
    ),
)
def echo(text: str) -> str:
    return text
