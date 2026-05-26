from openai import OpenAI
from anthropic import Anthropic
import json
from .schema import ChatResult, ToolCall
from configs.config import LLMConfig

class OpenAIClient:
    def __init__(self, llm_config: LLMConfig):
        self.model = llm_config.model
        self.temperature = llm_config.temperature
        self.max_tokens = llm_config.max_tokens
        self.client = OpenAI(
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
        )
    
    def get_response(self, messages, tools=None, tool_choice="auto"):
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_completion_tokens": self.max_tokens,
        }
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice

        response = self.client.chat.completions.create(**params)

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(ToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    args=json.loads(tc.function.arguments)
                ))

        return ChatResult(
            content=message.content,
            tool_calls=tool_calls,
            finish_reason=finish_reason
        )

    def build_assistant_message(self, result):
        msg = {"role": "assistant", "content": result.content}
        if result.has_tool_calls():
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.args, ensure_ascii=False),
                    },
                }
                for tc in result.tool_calls
            ]
        return msg

    def build_tool_result_message(self, tool_results):
        return [
            {
                "role": "tool",
                "tool_call_id": tc.id,
                "content": content,
            }
            for tc, content in tool_results
        ]

class AnthropicClient:
    def __init__(self, llm_config: LLMConfig):
        self.model = llm_config.model
        self.temperature = llm_config.temperature
        self.max_tokens = llm_config.max_tokens
        self.client = Anthropic(
            api_key=llm_config.api_key,
            base_url=llm_config.base_url,
        )

    def get_response(self, messages, tools=None):
        system_prompt = None
        filtered_messages = []
        for msg in messages:
            if msg.get("role") == "system":
                system_prompt = msg.get("content", "")
            else:
                filtered_messages.append(msg)

        params = {
            "model": self.model,
            "messages": filtered_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if system_prompt:
            params["system"] = system_prompt
        if tools:
            params["tools"] = [self._convert_tool_schema(t) for t in tools]

        response = self.client.messages.create(**params)

        tool_calls = []
        content = None
        for block in response.content:
            if block.type == "text":
                content = block.text
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    args=block.input,
                ))

        return ChatResult(
            content=content,
            tool_calls=tool_calls
        )

    def build_assistant_message(self, result):
        content = []
        if result.content:
            content.append({"type": "text", "text": result.content})
        for tc in result.tool_calls:
            content.append({
                "type": "tool_use",
                "id": tc.id,
                "name": tc.name,
                "input": tc.args,
            })
        return {"role": "assistant", "content": content}

    def build_tool_result_message(self, tool_results):
        return [
            {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": tc.id, "content": content}
                for tc, content in tool_results
            ],
            }
        ]
    
    def _convert_tool_schema(self, openai_schema):
      func = openai_schema["function"]
      return {
          "name": func["name"],
          "description": func.get("description", ""),
          "input_schema": func.get("parameters", {}),
      }
