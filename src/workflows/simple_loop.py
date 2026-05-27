from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .base import BaseWorkflow
import json

class SimpleWorkflow(BaseWorkflow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, messages):
        # Simple loop: 
        # LLM response -> 
        # execute tools -> 
        # LLM response with tool results -> 
        # repeat until no tool calls or max turns reached
        
        for turn in range(self.max_turns):
            result = self.client.get_response(messages, tools=self.tool_schemas)
            messages.append(self.client.build_assistant_message(result))

            if result.has_tool_calls():
                tool_results = []
                for tc in result.tool_calls:
                    output = await self._execute_tool(tc.name, tc.args)
                    tool_results.append((tc, output))
                messages.extend(self.client.build_tool_result_message(tool_results))
            else:
                self._log_messages(messages)
                return result.content
            
        return "对话轮数已达上限，未能得到最终回答。"