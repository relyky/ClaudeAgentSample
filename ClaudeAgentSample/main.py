import asyncio
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock, ToolUseBlock, ResultMessage
from claude_agent_sdk.types import HookMatcher
from load_env_files import is_debug_mode, load_env_files, get_env_value, get_env_value_as_int, validate_api_key
from utils import log_tool_use, check_escape_key, is_windows_platform

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
	max_turns = get_env_value_as_int("MAX_TURNS", None)

	system_prompt = """
You are a professional assistant whose native language is Taiwanese Traditional Chinese (zh-TW).

**Response Principles:**
- Demonstrate your work process.
- Omit greetings and small talk.
"""

## ※ system prompt 用英文效果更好。
# 	system_prompt = """
# 你是專業助手，母語為台灣繁體中文(zh-TW)。
# - 展示你的工作步驟。
# - 省略寒暄問候。
# """

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
		#       成功啟動條件:
		#       1. 使用 Claude Sonnet 4.5+ 或 Haiku 4.5+ 模型
		#       2. 有效的 Anthropic API 金鑰
		#       3. API 帳戶支援 WebSearch 功能
		#       4. 注意: 每 1,000 次搜尋收費 $10 USD (加上標準 token 費用)
		#       5. 目前僅在美國地區可用
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
		# 初始化 session 累積統計
		session_stats = {
			'total_input_tokens': 0,
			'total_output_tokens': 0,
			'total_cost_usd': 0.0,
			'turn_count': 0
		}

		print("=== Claude Agent 簡易互動模式 ===")
		print("輸入您的問題,或輸入 'exit' 或 'quit' 離開")
		if is_windows_platform():
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
				if is_windows_platform():
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

						# 處理 ResultMessage 以顯示 token 統計
						elif isinstance(message, ResultMessage):
							if is_debug_mode():
								print(f"\n[DEBUG:ResultMessage]", flush=True, end="")

							if message.usage:
								input_tokens = message.usage.get('input_tokens', 0)
								output_tokens = message.usage.get('output_tokens', 0)
								total_tokens = input_tokens + output_tokens

								# 更新累積統計
								session_stats['total_input_tokens'] += input_tokens
								session_stats['total_output_tokens'] += output_tokens
								session_stats['turn_count'] += 1

								if message.total_cost_usd:
									session_stats['total_cost_usd'] += message.total_cost_usd

								# 顯示當次統計
								print(f"\n📊 本輪 Tokens: 輸入={input_tokens} / 輸出={output_tokens} / 總計={total_tokens}", end="", flush=True)

								if message.total_cost_usd:
									print(f" | 💰 ${message.total_cost_usd:.6f} USD", end="", flush=True)

								# 顯示累積統計
								total_session_tokens = session_stats['total_input_tokens'] + session_stats['total_output_tokens']
								print(f"\n📈 累積統計: 輸入={session_stats['total_input_tokens']} / "
								      f"輸出={session_stats['total_output_tokens']} / "
								      f"總計={total_session_tokens} / "
								      f"輪次={session_stats['turn_count']}", end="", flush=True)

								if session_stats['total_cost_usd'] > 0:
									print(f" | 💰 累積成本: ${session_stats['total_cost_usd']:.6f} USD", end="", flush=True)

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
