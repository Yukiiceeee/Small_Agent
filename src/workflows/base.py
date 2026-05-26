from abc import ABC, abstractmethod
import json
from typing import List, Dict, Any

class BaseWorkflow(ABC):
    def __init__(self, client, tool_schemas, tool_map, max_turns):
        self.client = client
        self.tool_schemas = tool_schemas
        self.tool_map = tool_map
        self.max_turns = max_turns
    
    @abstractmethod
    def run(self, messages) -> str:
        """
          接收当前消息历史，执行编排逻辑，返回最终文本回复。
          内部自行管理 LLM 调用次数、工具调用、消息追加。
          """
        pass

    def _execute_tool(self, tool_name, tool_args):
        if tool_name not in self.tool_map:
            return f"未知工具: {tool_name}"
        try:
              return self.tool_map[tool_name](tool_args)
        except Exception as e:
              return json.dumps({"error": str(e)}, ensure_ascii=False)

    def _log_messages(self, messages):
        print("\n========== Messages Log ==========")
        for i, msg in enumerate(messages):
            role = msg.get("role", "?")
            content = msg.get("content")

            if role == "system":
                print(f"[{i}] SYSTEM: {content[:80]}{'...' if len(content) > 80 else ''}")

            elif role == "user":
                if isinstance(content, str):
                    print(f"[{i}] USER: {content}")
                elif isinstance(content, list):
                    types = [b.get("type") for b in content]
                    print(f"[{i}] USER (tool_result): {types}")
                    for b in content:
                        if b.get("type") == "tool_result":
                            res = b.get("content", "")
                            print(f"     └─ {b.get('tool_use_id')}: {res[:100]}")

            elif role == "assistant":
                if isinstance(content, str):
                    print(f"[{i}] ASSISTANT: {content[:200]}")
                elif isinstance(content, list):
                    for b in content:
                        if b.get("type") == "text":
                            print(f"[{i}] ASSISTANT: {b['text'][:200]}")
                        elif b.get("type") == "tool_use":
                            print(f"[{i}] TOOL_CALL: {b['name']}({json.dumps(b.get('input', {}), ensure_ascii=False)})")
                tool_calls = msg.get("tool_calls")
                if tool_calls:
                    for tc in tool_calls:
                        func = tc.get("function", {})
                        print(f"[{i}] TOOL_CALL: {func.get('name')}({func.get('arguments', '')})")

            elif role == "tool":
                tid = msg.get("tool_call_id", "?")
                print(f"[{i}] TOOL_RESULT ({tid}): {str(content)[:100]}")

        print("==================================\n")