import asyncio
from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKClient, AssistantMessage, TextBlock, ResultMessage, ToolUseBlock

async def main():
  # ClaudeAgentOptions 用於設定 AI 模型的行為參數
	options = ClaudeAgentOptions(
    system_prompt="你是一個樂於助人的助手。你的母語是中文以台灣口語為主。展示你的工作步驟。",  # 定義 AI 的角色與行為準則
    max_turns=None,  # 不限制對話輪次（適用於 agent 模式，單次查詢時無影響）
    model="claude-sonnet-4-5-20250929",  # 指定使用的 Claude 模型版本
		#api_key="your_claude_api_key_here",  # 請替換為您的 Claude API 金鑰		
    # 設定並允許外部 MCP 服務與工具
		mcp_servers={
      "fetch":{
        "command":"uvx",
        "args":["mcp-server-fetch"]
      }
    },
    allowed_tools=["mcp__fetch__fetch"]
	)

	# 使用非同步上下文管理器建立 Claude SDK 客戶端
	async with ClaudeSDKClient(options=options) as client:
		print("=== Claude Agent 簡易互動模式 ===")
		print("輸入您的問題,或輸入 'exit' 或 'quit' 離開\n")

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

				# 處理回應
				print("Claude: ", end="", flush=True)
				has_content = False
				async for message in client.receive_response():
					if isinstance(message, AssistantMessage):
						for block in message.content:
							if isinstance(block, TextBlock):
								print(block.text, end="", flush=True)
								has_content = True
							elif isinstance(block, ToolUseBlock):
								# 顯示工具使用訊息
								print(f"\n[使用工具: {block.name}]", end="", flush=True)
								has_content = True

				if not has_content:
					print("(無回應內容)", end="", flush=True)
				print("\n")  # 換行以分隔對話

			except Exception as e:
				print(f"\n錯誤: {type(e).__name__}: {e}\n", flush=True)
				# 繼續執行,不要中斷整個程式

if __name__ == "__main__":
	asyncio.run(main())
