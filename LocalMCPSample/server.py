"""
簡單的 MCP Server 範例

此範例展示如何建立一個基本的 MCP Server。
"""
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("local-mcp-sample")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[local-mcp-sample] Adding {a} and {b}")
    return (a + b)

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print(f"[local-mcp-sample] Greeting for {name}")
    return f"Hello, {name}!"
