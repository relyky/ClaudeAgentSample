# ClaudeAgentSample

使用 **Claude Agent SDK** 的 Python 互動式命令列應用程式。

## 功能特色

- 透過命令列與 Claude AI 進行互動式對話
- 整合 MCP (Model Context Protocol) 支援外部工具呼叫
- 支援多輪對話與工具使用追蹤

## 環境需求

- **Python 3.14+**
- **uv** 套件管理器

## 核心依賴

- `claude-agent-sdk==0.1.7` - Claude Agent 官方 SDK
- `python-dotenv==1.2.1` - 環境變數管理

## 環境設定

環境變數優先順序: `.env.dev` > `.env`

- `.env` - 基礎設定範本(已納入版控)
- `.env.dev` - 開發環境設定(已納入版控)

## 快速開始

```bash
# 安裝依賴
uv sync

# 啟動互動式對話
uv run main.py
```

## 專案架構

- **`main.py`** - 應用程式進入點,實作互動式對話迴圈與 MCP fetch 伺服器整合
- **`load_env_files.py`** - 環境變數載入與驗證模組

## MCP 整合

使用 `uvx mcp-server-fetch` 提供網路抓取能力,在 `main.py` 的 `ClaudeAgentOptions` 中設定。
