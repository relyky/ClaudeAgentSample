import asyncio
import sys
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock, ToolUseBlock
from claude_agent_sdk.types import PreToolUseHookInput, PostToolUseHookInput, HookContext, SyncHookJSONOutput, HookMatcher
from load_env_files import is_debug_mode, load_env_files, get_env_value, get_env_value_as_int, validate_api_key

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

async def main():
	# 載入環境變數
	load_env_files()

	if is_debug_mode():
		print("[開發模式]")
	
	# 驗證 API 金鑰，當非開發模式才進行檢查。
	if not is_debug_mode():
		is_valid, error_msg = validate_api_key()
		if not is_valid:
			print(f"❌ 錯誤: {error_msg}")
			print("請在 .env 檔案中設定您的 API 金鑰")
			return

	# 讀取參數值
	model = get_env_value("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
	#system_prompt = get_env_value("CLAUDE_SYSTEM_PROMPT","你是一個樂於助人的助手。你的母語是中文(台灣口語)。展示你的工作步驟。")
	max_turns = get_env_value_as_int("MAX_TURNS", None)

	system_prompt = """
你是專業助手，母語為台灣繁體中文(zh-TW)。

**回應原則：**
- 直接給結論，必要時再展開說明
- 條列式呈現重點
- 顯示關鍵推理步
- 省略寒暄問候

**結尾格式：**
用一行文字總結本次 tokens 消耗（輸入/輸出/總計）
"""

	# ClaudeAgentOptions 用於設定 AI 模型的行為參數
	options = ClaudeAgentOptions(
		system_prompt=system_prompt,  # 定義 AI 的角色與行為準則
		max_turns=max_turns,  # 不限制對話輪次（適用於 agent 模式，單次查詢時無影響）
		model=model,  # 指定使用的 Claude 模型版本
		# 設定並允許外部 MCP 服務與工具
		mcp_servers={
			"fetch":{
				"command":"uvx",
				"args":["mcp-server-fetch"]
			},
			"local-mcp-sample":{
				"command":"uv",
				"args":["run", "--directory", "..\\LocalMCPSample", "mcp", "run", "server.py"]
			}
		},
		# 允許的工具清單:
		# - mcp__fetch__fetch: 透過 MCP server 提供的網頁抓取工具
		# - mcp__local-mcp-sample__add: 本地自訂 MCP server 的加法工具 (LocalMCPSample/server.py)
		# - mcp__local-mcp-sample__get_weather: 本地自訂 MCP server 的天氣查詢工具 (LocalMCPSample/server.py)
		# - web_search: Claude API 原生網路搜尋工具(無需 MCP server)
		#   成功啟動條件:
		#   1. 使用 Claude Sonnet 4.5+ 或 Haiku 4.5+ 模型
		#   2. 有效的 Anthropic API 金鑰
		#   3. API 帳戶支援 WebSearch 功能
		#   4. 注意: 每 1,000 次搜尋收費 $10 USD (加上標準 token 費用)
		#   5. 目前僅在美國地區可用
		allowed_tools=[
			"mcp__fetch__fetch",
			"mcp__local-mcp-sample__add",
			"mcp__local-mcp-sample__get_weather",
			"web_search"
		],
		# 配置 PreToolUse 和 PostToolUse hooks 用於記錄工具使用情況
		hooks={
			"PreToolUse": [
				HookMatcher(
					matcher=None,  # None 表示匹配所有工具
					hooks=[log_tool_use],
				)
			],
			"PostToolUse": [
				HookMatcher(
					matcher=None,  # None 表示匹配所有工具
					hooks=[log_tool_use],
				)
			],
		}
	)

	print(f"✓ 使用模型: {model}\n")
	print(f"✓ system_prompt: {system_prompt}\n")

	# 使用非同步上下文管理器建立 Claude SDK 客戶端
	async with ClaudeSDKClient(options=options) as client:
		print("=== Claude Agent 簡易互動模式 ===")
		print("輸入您的問題,或輸入 'exit' 或 'quit' 離開")
		if msvcrt is not None:
			print("在 AI 回應時按 ESC 鍵可中斷運算")
		print()

		while True:
			# 取得使用者輸入
			try:
				user_input = input("您: ").strip()
			except EOFError:
				print("\n再見!")
				break
			except KeyboardInterrupt:
				print("\n\n使用者中斷,再見!")
				break

			# 檢查是否要離開
			if user_input.lower() in ['exit', 'quit', '離開', '退出']:
				print("再見!")
				break

			# 略過空白輸入
			if not user_input:
				continue

			# 發送問題給 Claude 並處理回應
			try:
				await client.query(user_input)

				# 設定取消標記與啟動 ESC 鍵監聽
				cancel_flag = {'cancelled': False, 'stop': False}
				escape_task = asyncio.create_task(check_escape_key(cancel_flag))

				# 處理回應
				print("Claude: ", end="", flush=True)
				if msvcrt is not None:
					print("(按 ESC 鍵中斷) ", end="", flush=True)
				has_content = False
				interrupted = False

				try:
					async for message in client.receive_response():
						# 檢查是否按下 ESC 鍵
						if cancel_flag.get('cancelled', False):
							interrupted = True
							print("\n\n⚠️  [使用者按下 ESC，中斷回應]", flush=True)
							break

						# 顯示回應內容
						if isinstance(message, AssistantMessage):
							for block in message.content:
								if isinstance(block, TextBlock):
									if is_debug_mode():
										print(f"\n[DEBUG:TextBlock]", flush=True)
									print(block.text, end="", flush=True)
									has_content = True  # 有文字回應
								elif isinstance(block, ToolUseBlock):
									# 工具使用訊息由 PreToolUse/PostToolUse hooks 處理
									if is_debug_mode():
										print(f"\n[DEBUG:ToolUseBlock:{block.name}]", flush=True)
									has_content = True # 有工具使用回應

					# 回應結束後的處理
					if not has_content and not interrupted:
						print("(無回應內容)", end="", flush=True)
					if not interrupted:
						print("\n")  # 換行以分隔對話

				finally:
					# 停止 ESC 鍵監聽任務
					cancel_flag['stop'] = True
					try:
						await asyncio.wait_for(escape_task, timeout=1.0)
					except asyncio.TimeoutError:
						escape_task.cancel()

			except Exception as e:
				print(f"\n錯誤: {type(e).__name__}: {e}\n", flush=True)
				# 繼續執行,不要中斷整個程式

if __name__ == "__main__":
	asyncio.run(main())
