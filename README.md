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
