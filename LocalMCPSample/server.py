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
    return (a + b)

# Add a dynamic greeting resource
# 資源預設就是開放的，不需要像 tools 設定授權。
# 但資源一般是間接被使用的。也可以明確的提出資源 URL 來取得資源內容。
# 例如： prompt> 查看資源 @local-mcp-sample:greeting://Steven 
# 輸出:
# **資源資訊：**
# - **URI**: `greeting://Steven`
# - **MIME 類型**: `text/plain`
# - **內容**: `Hello, Steven!`
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
