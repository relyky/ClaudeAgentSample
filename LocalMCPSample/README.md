# LocalMCPSample

本專案用於開發本地 MCP (Model Context Protocol) Server 範例。

## 專案目的

提供 MCP Server 開發的範例與實驗環境,幫助理解如何建立自訂的 MCP Server 並與 Claude Agent 整合。

## 環境需求

- **Python 3.14+**
- **uv** 套件管理器

## 快速開始

```bash
# 安裝依賴
uv sync

# 啟動 MCP Server (範例)
uv run server.py
```

## 開發指南

(待補充)

## 參考資源
- [使用 uv 輔助開發 MCP 伺服器並安裝到 Claude Desktop 與 VS Code](https://blog.miniasp.com/post/2025/04/01/Write-your-own-MCP-server-using-uv-and-Python)
- [MCP Resources & Templates](https://gofastmcp.com/servers/resources)
- [MCP Resources explained (and how they differ from MCP Tools)](https://medium.com/@laurentkubaski/mcp-resources-explained-and-how-they-differ-from-mcp-tools-096f9d15f767)
- [MCP 官方文件](https://modelcontextprotocol.io/)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [FastMCP 官方文件](https://github.com/anthropics/anthropic-sdk-python)
