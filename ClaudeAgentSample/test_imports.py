"""測試 utils 模組的 imports 是否正常"""
try:
    from utils import log_tool_use, check_escape_key, is_windows_platform

    print("[OK] Successfully imported log_tool_use")
    print("[OK] Successfully imported check_escape_key")
    print("[OK] Successfully imported is_windows_platform")

    # 測試 is_windows_platform 函式
    result = is_windows_platform()
    print(f"[OK] is_windows_platform() returned: {result}")

    print("\n[SUCCESS] All imports passed!")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
