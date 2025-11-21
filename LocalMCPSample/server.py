"""
簡單的 MCP Server 範例

此範例展示如何建立一個基本的 MCP Server。
"""
import asyncio
import aiohttp
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("local-mcp-sample")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return (a + b)

# Add a weather tool
@mcp.tool()
async def get_weather(latitude: float, longitude: float) -> str:
    """Get current temperature for a location using coordinates

    Args:
        latitude: Latitude coordinate (e.g., 25.0330 for Taipei)
        longitude: Longitude coordinate (e.g., 121.5654 for Taipei)

    Returns:
        Current temperature in Fahrenheit
    """
    # Call Open-Meteo weather API (free, no API key required)
    try:
        timeout = aiohttp.ClientTimeout(total=10)  # 10 秒超時
        async with aiohttp.ClientSession(timeout=timeout) as session:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m&temperature_unit=fahrenheit"
            async with session.get(url) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return f"Error: Unable to fetch weather data (HTTP {response.status}): {error_text[:100]}"

                data = await response.json()

                # Extract temperature from response
                temperature = data.get('current', {}).get('temperature_2m')

                if temperature is None:
                    return f"Error: Temperature data not available in response: {data}"

                return f"Temperature at ({latitude}, {longitude}): {temperature}°F"

    except aiohttp.ClientError as e:
        return f"Error: Network request failed: {str(e)}"
    except asyncio.TimeoutError:
        return "Error: Request timed out (10 seconds)"
    except Exception as e:
        return f"Error: Unexpected error occurred: {str(e)}"

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
