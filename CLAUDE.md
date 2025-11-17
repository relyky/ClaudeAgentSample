# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個使用 **uv** 套件管理器的 Python 專案。專案目前是一個簡單的命令列應用程式。

## Python 版本需求

- **Python 3.14+** (定義於 `.python-version` 和 `pyproject.toml`)

## 套件管理 (使用 uv)

本專案使用 [uv](https://github.com/astral-sh/uv) 作為套件管理器,而非傳統的 pip。

### 安裝相依套件
```bash
uv sync
```

### 新增套件
```bash
# 新增一般依賴
uv add package-name

# 新增開發依賴
uv add --dev package-name
```

### 移除套件
```bash
uv remove package-name
```

## 常用指令

### 執行程式
```bash
uv run main.py
```

uv 會自動管理虛擬環境(.venv),無需手動啟動。

### 執行任意 Python 指令
```bash
uv run python your_script.py
```

## 專案結構

目前專案採用扁平結構:
- `main.py`: 主要進入點
- `pyproject.toml`: 專案配置和依賴管理
- `uv.lock`: 依賴鎖定檔(確保可重現的安裝)
- `.python-version`: Python 版本規範
- `.venv/`: 虛擬環境(由 uv 自動管理,已被 .gitignore 忽略)

## 開發注意事項

### 虛擬環境
uv 會自動在 `.venv` 目錄建立和管理虛擬環境。不需要手動建立或啟動虛擬環境。

### 依賴管理
所有依賴都在 `pyproject.toml` 中定義。修改依賴後,`uv.lock` 會自動更新以確保一致性。
