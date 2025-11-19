# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個使用 **Claude Agent SDK** 的 Python 互動式命令列應用程式,採用 **uv** 作為套件管理器。

### 核心功能
- 透過命令列與 Claude AI 進行互動式對話
- 整合 MCP (Model Context Protocol) 支援外部工具呼叫
- 支援多輪對話與工具使用追蹤
- 使用環境變數管理 API 金鑰和應用程式設定

## Python 版本需求

- **Python 3.14+** (定義於 `.python-version` 和 `pyproject.toml`)

## 核心依賴

- `claude-agent-sdk==0.1.7` - Claude Agent 官方 SDK
- `python-dotenv==1.2.1` - 環境變數管理

## 環境變數設定

專案使用多層環境變數設定機制:

1. **`.env`** - 基礎設定檔範本(已納入版控,使用預設/範例值)
2. **`.env.dev`** - 開發環境設定檔(已納入版控,包含開發團隊共用設定)

### 首次設定步驟

```bash
# 1. 複製範本檔案
cp .env .env.dev

# 2. 編輯 .env.dev 並填入實際的設定值
# ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 主要環境變數

- `ANTHROPIC_API_KEY` - Anthropic API 金鑰 (必填,從 https://console.anthropic.com/settings/keys 取得)
- `CLAUDE_MODEL` - Claude 模型版本 (預設: `claude-sonnet-4-5-20250929`)
- `CLAUDE_SYSTEM_PROMPT` - 系統提示詞,定義 AI 行為
- `MAX_TURNS` - 對話輪次限制 (留空表示無限制)
- `DEBUG` - 除錯模式 (`true`/`false`)

## 套件管理 (使用 uv)

本專案使用 [uv](https://github.com/astral-sh/uv) 作為套件管理器,而非傳統的 pip。

### 安裝相依套件

```bash
# 使用 uv 同步依賴
uv sync

# 或使用 requirements.txt 安裝
uv pip install -r requirements.txt
```

### 新增/移除套件

```bash
# 新增套件 (會更新 requirements.txt)
uv add package-name

# 移除套件
uv remove package-name
```

## 常用指令

### 執行應用程式

```bash
# 啟動互動式對話
uv run main.py
```

應用程式啟動後:
- 輸入問題與 Claude 互動
- 輸入 `exit` 或 `quit` 離開
- 支援 Ctrl+C 中斷對話

## 專案架構

### 核心檔案

- **`main.py`** - 應用程式進入點
  - 使用 `asyncio` 處理非同步 Claude API 呼叫
  - 實作互動式對話迴圈
  - 整合 MCP fetch 伺服器用於網路請求
  - 處理 `AssistantMessage`、`TextBlock` 和 `ToolUseBlock` 等訊息類型

- **`load_env_files.py`** - 環境變數載入模組
  - 提供 `load_env_files()` 載入 .env 檔案
  - 提供 `get_env_value()` / `get_env_value_as_int()` / `get_env_value_as_bool()` 取得環境變數
  - 提供 `validate_api_key()` 驗證 API 金鑰格式
  - 提供 `is_debug_mode()` 判斷除錯模式

### MCP 整合

專案已整合 MCP (Model Context Protocol) 伺服器:
- **`fetch`** - 使用 `uvx mcp-server-fetch` 提供網路抓取能力
- 在 `main.py` 的 `ClaudeAgentOptions` 中設定 `mcp_servers`
- 允許的工具: `mcp__fetch__fetch`

### 設定檔

- **`pyproject.toml`** - 專案元資料與依賴定義
- **`requirements.txt`** - 套件依賴清單
- **`.python-version`** - Python 版本規範
- **`.env` / `.env.dev`** - 環境變數設定

## 開發注意事項

### API 金鑰與環境變數
- `.env.dev` 已納入版本控制,用於團隊共享開發設定
- API 金鑰必須以 `sk-` 開頭(Anthropic 格式)
- 非 DEBUG 模式時會自動驗證 API 金鑰

### 虛擬環境
uv 會自動在 `.venv` 目錄建立和管理虛擬環境。不需要手動建立或啟動虛擬環境。

### 訊息處理流程
1. 使用者輸入問題 → `client.query()`
2. 透過 `client.receive_response()` 串流接收回應
3. 處理不同類型的訊息區塊:
   - `TextBlock` - 顯示文字回應
   - `ToolUseBlock` - 顯示工具呼叫資訊
4. 錯誤處理但不中斷對話
