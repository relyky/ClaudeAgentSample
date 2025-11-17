# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個 Python 命令列工具專案。

## 開發環境設定

### 安裝相依套件
```bash
pip install -r requirements.txt
```

### 開發模式安裝(如果使用 setup.py 或 pyproject.toml)
```bash
pip install -e .
```

## 常用指令

### 執行程式
```bash
python main.py
```

### 執行測試
```bash
# 使用 pytest
pytest

# 執行單一測試檔案
pytest tests/test_specific.py

# 執行單一測試函數
pytest tests/test_specific.py::test_function_name

# 顯示詳細輸出
pytest -v

# 顯示測試覆蓋率
pytest --cov
```

### 程式碼品質檢查
```bash
# 使用 pylint
pylint **/*.py

# 使用 flake8
flake8 .

# 使用 black 格式化程式碼
black .

# 使用 mypy 進行型別檢查
mypy .
```

## 專案架構

### 目錄結構
- `main.py` 或 `cli.py`: CLI 進入點
- `src/`: 主要程式碼目錄
- `tests/`: 測試檔案目錄
- `requirements.txt`: 專案相依套件清單
- `README.md`: 專案說明文件

### CLI 框架
如果使用 CLI 框架(如 Click、argparse、Typer),請在實作新指令時遵循現有的模式。

## 開發注意事項

### Python 版本
檢查 `requirements.txt` 或 `pyproject.toml` 以確認專案支援的 Python 版本。

### 虛擬環境
建議使用虛擬環境進行開發:
```bash
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境 (Windows)
venv\Scripts\activate

# 啟動虛擬環境 (Linux/Mac)
source venv/bin/activate
```
