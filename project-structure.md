# ClaudeAgentSample 專案結構圖

## 資料流向

```mermaid
sequenceDiagram
    participant User as 👤 使用者
    participant CLI as ClaudeAgentSample<br/>(main.py)
    participant SDK as Claude Agent SDK
    participant MCP as MCP Server<br/>(LocalMCPSample)
    participant Claude as 🤖 Claude AI

    User->>CLI: 輸入指令/問題
    CLI->>SDK: 初始化 Agent
    SDK->>MCP: 載入 MCP 工具
    MCP-->>SDK: 註冊工具 (get_weather 等)
    SDK->>Claude: 發送請求 + MCP 工具
    Claude->>Claude: 分析需求

    alt 需要使用工具
        Claude->>MCP: 呼叫 MCP 工具
        MCP->>MCP: 執行工具邏輯
        MCP-->>Claude: 回傳結果
    end

    Claude-->>SDK: 生成回應
    SDK-->>CLI: 回傳結果
    CLI-->>User: 顯示回應

    Note over User,Claude: 支援多輪對話循環
```

## 詳細目錄結構

```
ClaudeAgentSample/
├── 📄 CLAUDE.md                                # 通用開發指引
├── 📄 README.md                                # 方案說明文件
├── 📄 .gitignore                               # Git 忽略設定
├── 📊 The Agentic AI Simple Stack.pptx         # 簡報檔案
│
├── 📁 .claude/                                 # Claude Code 配置
│   ├── 📄 settings.local.json                  # 本地設定
│   └── 📁 agents/                              # 自訂 Agent
│       ├── 📄 code-reviewer.md                 # 程式碼審查專家
│       ├── 📄 data-scientist.md                # 資料科學專家
│       ├── 📄 debugger.md                      # 除錯專家
│       ├── 📄 prd-writer.md                    # PRD 撰寫專家
│       ├── 📄 steering-architect.md            # 專案架構師
│       ├── 📄 strategic-planner.md             # 策略規劃師
│       └── 📄 task-executor.md                 # 任務執行器
│
├── 📁 ClaudeAgentSample/                       # Claude Agent SDK 應用
│   ├── 📄 pyproject.toml                       # 依賴: claude-agent-sdk, mcp, dotenv
│   ├── 📄 CLAUDE.md                            # 開發指引
│   ├── 📄 README.md
│   ├── 📄 .python-version                      # 3.14+
│   ├── 📄 requirements.txt
│   ├── 📄 uv.lock
│   ├── 🔧 .env                                 # 基礎配置
│   ├── 🔧 .env.dev                             # 開發配置
│   ├── 🐍 main.py                              # 互動式 CLI 主程式
│   ├── 🐍 load_env_files.py                    # 環境變數載入
│   └── 📁 .venv/
│
└── 📁 LocalMCPSample/                          # MCP Server 範例
    ├── 📄 pyproject.toml                       # 依賴: mcp, aiohttp
    ├── 📄 README.md
    ├── 📄 .python-version                      # 3.14+
    ├── 📄 uv.lock
    ├── 🐍 main.py                              # Server 啟動入口
    ├── 🐍 server.py                            # MCP Server 實作 (get_weather)
    └── 📁 .venv/
```

## 核心功能模組

```mermaid
graph TD
    subgraph "ClaudeAgentSample/main.py"
        M1[互動式對話迴圈]
        M2[MCP Fetch Server 整合]
        M3[多輪對話追蹤]
        M4[工具呼叫處理]
    end

    subgraph "ClaudeAgentSample/load_env_files.py"
        E1[載入 .env.dev]
        E2[載入 .env]
        E3[環境變數驗證]
        E1 -.優先.-> E2
    end

    subgraph "LocalMCPSample/server.py"
        S1[MCP Server 初始化]
        S2[get_weather 工具]
        S3[資源與提示定義]
        S4[StdIO 傳輸]
    end

    M2 --> S1
    M1 --> M4
    M4 --> S2

    style M1 fill:#e8f5e9
    style S1 fill:#f3e5f5
    style E1 fill:#fff4e6
```
