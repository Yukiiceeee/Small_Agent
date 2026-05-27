from .base import BaseWorkflow

class PlanExecuteWorkflow(BaseWorkflow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, messages):
        # plan & execute workflow:
        # 1. plan (think and generate a plan)
        # 2. execute (call tools according to the plan)
        # 3. observe (get tool results)
        # 4. repeat until we have enough information to answer the question

        # plan phase
        plan_tools = [tool for tool in self.tool_schemas if tool["function"]["name"] == "create_plan"]
        
        result = self.client.get_response(messages, tools=plan_tools, tool_choice="required")
        messages.append(self.client.build_assistant_message(result))
        if result.has_tool_calls():
            for tc in result.tool_calls:
                output = await self._execute_tool(tc.name, tc.args)
                messages.extend(self.client.build_tool_result_message([(tc, output)]))
        
        # execute phase
        messages.append({"role": "user", "content": "根据上面的计划，借助工具一步步执行，最终返回答案。"})
        for turn in range(self.max_turns):
            result = self.client.get_response(messages, tools=self.tool_schemas)
            messages.append(self.client.build_assistant_message(result))

            if result.has_tool_calls():
                for tc in result.tool_calls:
                    output = await self._execute_tool(tc.name, tc.args)
                    messages.extend(self.client.build_tool_result_message([(tc, output)]))
            else:
                self._log_messages(messages)
                return result.content
