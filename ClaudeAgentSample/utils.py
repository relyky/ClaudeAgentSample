import asyncio
import sys
from claude_agent_sdk.types import PreToolUseHookInput, PostToolUseHookInput, HookContext, SyncHookJSONOutput

# 平台相依的 import - Windows 限定
if sys.platform == 'win32':
	import msvcrt
else:
	msvcrt = None

async def log_tool_use(
	input_data: PreToolUseHookInput | PostToolUseHookInput,
	tool_use_id: str | None,
	context: HookContext,
) -> SyncHookJSONOutput:
	"""通用 hook: 在工具執行前後以簡潔模式通知使用者"""
	tool_name = input_data["tool_name"]
	hook_event = input_data["hook_event_name"]

	# 根據不同的 hook 類型顯示不同的訊息
	if hook_event == "PreToolUse":
		print(f"\n[Hooks.PreToolUse : 🔧 {tool_name}]", flush=True)
	elif hook_event == "PostToolUse":
		print(f"[Hooks.PostToolUse: ✅ {tool_name}]", flush=True)

	return {
		"hookEventName": hook_event,
		"continue_": True,
	}

async def check_escape_key(cancel_flag: dict):
	"""背景任務: 檢查是否按下 ESC 鍵 (僅支援 Windows)"""
	# 非 Windows 平台不支援 ESC 鍵檢測
	if msvcrt is None:
		return

	loop = asyncio.get_event_loop()

	def check_key():
		"""檢查鍵盤輸入 (在執行器中運行以避免阻塞)"""
		if msvcrt.kbhit():
			key = msvcrt.getch()
			return key == b'\x1b'  # ESC 鍵的編碼
		return False

	while not cancel_flag.get('stop', False):
		try:
			if await loop.run_in_executor(None, check_key):
				cancel_flag['cancelled'] = True
				return
			await asyncio.sleep(0.05)  # 每 50ms 檢查一次
		except Exception:
			break

def is_windows_platform() -> bool:
	"""檢查是否為 Windows 平台（支援 ESC 鍵檢測）"""
	return msvcrt is not None

__all__ = ['log_tool_use', 'check_escape_key', 'is_windows_platform']
