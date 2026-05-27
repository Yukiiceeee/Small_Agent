from .base import BaseWorkflow

class ReActWorkflow(BaseWorkflow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, messages):
        # ReAct workflow:
        # 1. Think
        # 2. Act (call tool)
        # 3. Observe (get tool result)
        # Repeat until we have enough information to answer the user

        for turn in range(self.max_turns):
            result = self.client.get_response(messages, tools=self.tool_schemas)
            
            if result.content:
                print(f"  [Thought] {result.content}")
            messages.append(self.client.build_assistant_message(result))

            if result.has_tool_calls():
                for tc in result.tool_calls:
                    print(f"  [Action] Calling tool: {tc.name} with args: {tc.args}")
                    output = await self._execute_tool(tc.name, tc.args)
                    print(f"  [Observation] Tool output: {output}")
                    messages.extend(self.client.build_tool_result_message([(tc, output)]))
            else:
                self._log_messages(messages)
                return result.content
            
        return "对话轮数已达上限，未能得到最终回答。"
