# Claude Agent 開發方案

本方案包含兩個專案,用於學習與實驗 Claude Agent SDK 及 MCP (Model Context Protocol) 開發。

## 專案結構

```
ClaudeAgentSample/          # 根目錄
├── ClaudeAgentSample/      # Claude Agent SDK 互動式應用程式
└── LocalMCPSample/         # 本地 MCP Server 開發範例
```

## 專案說明

### 1. ClaudeAgentSample

使用 Claude Agent SDK 的 Python 互動式命令列應用程式,展示如何與 Claude AI 進行對話並整合 MCP 工具。

- **主要功能**: 互動式對話、MCP 工具整合、多輪對話追蹤
- **技術棧**: Python 3.14+, claude-agent-sdk, uv

詳細說明請參閱 [ClaudeAgentSample/README.md](./ClaudeAgentSample/README.md)

### 2. LocalMCPSample

本地 MCP Server 開發範例專案,用於學習如何建立自訂的 MCP Server。

- **主要目的**: MCP Server 開發實驗與範例
- **技術棧**: Python 3.14+, mcp, uv

詳細說明請參閱 [LocalMCPSample/README.md](./LocalMCPSample/README.md)

## 環境需求

- **Python 3.14+**
- **uv** 套件管理器

## 快速開始

### 執行 ClaudeAgentSample

```bash
cd ClaudeAgentSample
uv sync
uv run main.py
```

### 執行 LocalMCPSample

```bash
cd LocalMCPSample
uv sync
uv run server.py
```

## 參考資源

- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Anthropic Documentation](https://docs.anthropic.com/)


# SIT-測試提問

```
您: 

### 測試記憶能力 ###
我叫 John
我是誰？你有我的相關資訊？

### 測試第三方套件 mcp__fetch__fetch 能力（無 web_search）###
用一段話總結此網址內容 https://rely-ky.gitbook.io/net8/cloud/redis-yan-jiu-bi-ji

### 測試 custom mcp server: 加法, 查詢天氣, resource ###
3 + 4
use local-mcp-sample, 3 + 7
上網查詢今天新北市天氣
向 Steven 問安
查看資源 @local-mcp-sample:greeting://Steven
向 Steven 問安

What's the weather in San Francisco?
use local-mcp-sample, 查詢天氣,地點經緯度座標 25.0330° N, 121.5654° E

台北現在的溫度是多少？經緯度是 25.0330, 121.5654
舊金山現在天氣如何?
```