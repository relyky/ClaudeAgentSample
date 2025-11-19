"""
環境變數載入模組

此模組負責載入和管理環境變數,支援多個環境檔案的優先順序設定。
"""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_env_files():
	"""
	載入環境變數檔案
	優先順序: .env.local > .env

	.env        - 基礎設定檔 (可提交到版本控制)
	.env.local  - 本地設定檔 (包含敏感資訊,不提交到版本控制)
	"""
	# 取得當前模組所在目錄作為專案根目錄
	project_root = Path(__file__).parent

	env_path = project_root / ".env"
	env_local_path = project_root / ".env.local"

	# 先載入 .env (基礎設定)
	if env_path.exists():
		load_dotenv(env_path)
		print(f"✓ 已載入 {env_path}")
	else:
		print(f"⚠ 找不到 {env_path}")

	# 再載入 .env.local (覆蓋本地設定)
	if env_local_path.exists():
		load_dotenv(env_local_path, override=True)
		print(f"✓ 已載入 {env_local_path}")


def get_env_value(key: str, default: str = None) -> str:
	"""
	取得環境變數值

	Args:
		key: 環境變數鍵名
		default: 預設值 (當環境變數不存在或為空字串時使用)

	Returns:
		環境變數值,如果不存在或為空則返回預設值

	Example:
		>>> get_env_value("API_KEY", "default-key")
		'your-api-key'

		>>> get_env_value("MISSING_KEY", "fallback")
		'fallback'
	"""
	value = os.getenv(key, default)

	# 如果值是空字串,也視為未設定,返回預設值
	if value == "":
		return default

	return value


def validate_api_key(api_key: str = None) -> tuple[bool, str]:
	"""
	驗證 API 金鑰是否有效設定

	Args:
		api_key: 要驗證的 API 金鑰,如果為 None 則從環境變數讀取

	Returns:
		(是否有效, 錯誤訊息)

	Example:
		>>> is_valid, error = validate_api_key()
		>>> if not is_valid:
		...     print(error)
	"""
	if api_key is None:
		api_key = get_env_value("ANTHROPIC_API_KEY")

	if not api_key:
		return False, "未設定 ANTHROPIC_API_KEY 環境變數"

	if api_key == "your-api-key-here":
		return False, "請將 ANTHROPIC_API_KEY 更換為實際的 API 金鑰"

	# 簡單檢查格式 (Anthropic API 金鑰通常以 sk- 開頭)
	if not api_key.startswith("sk-"):
		return False, "API 金鑰格式可能不正確 (應以 'sk-' 開頭)"

	return True, ""

def get_env_value_as_int(key: str, default: int = None) -> int:
	"""
	取得環境變數值並轉換為整數

	Args:
		key: 環境變數鍵名
		default: 預設值 (當環境變數不存在、為空或無法轉換時使用)

	Returns:
		整數值,如果無法轉換則返回預設值

	Example:
		>>> get_env_value_as_int("MAX_TURNS", 10)
		10

		>>> get_env_value_as_int("PORT", 8080)
		8080
	"""
	value_str = get_env_value(key, "")

	# 如果環境變數不存在或為空,返回預設值
	if not value_str:
		return default

	# 嘗試轉換為整數
	try:
		return int(value_str)
	except ValueError:
		print(f"⚠ 警告: 環境變數 {key}='{value_str}' 無法轉換為整數,使用預設值 {default}")
		return default
