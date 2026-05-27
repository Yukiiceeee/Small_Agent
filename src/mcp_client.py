import json
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPManager:
    def __init__(self):
        self._exit_stack = AsyncExitStack()
        self._tool_to_session: dict[str, ClientSession] = {}
        self.tools = []

    async def connect(self, server_configs: list[dict]) -> None:
        for config in server_configs:
            params = StdioServerParameters(
                command=config["command"],
                args=config["args"]
            )
            transport = await self._exit_stack.enter_async_context(
                stdio_client(params)
            )
            read_stream, write_stream = transport

            session = await self._exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )

            await session.initialize()
            response = await session.list_tools()
            for tool in response.tools:
                self._tool_to_session[tool.name] = session
                self.tools.append(tool)
            
            print(f"Connected to {config['name']} server, found tools: {[t.name for t in response.tools]}")

    def get_openai_schemas(self) -> list[dict]:
        """将 MCP tool schema 转换为 OpenAI function calling 格式"""
        openai_schemas = []
        for tool in self.tools:
            schema = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            openai_schemas.append(schema)
        return openai_schemas

    async def call_tool(self, name: str, args: dict) -> str:
        """根据工具名路由到正确的 Server 并执行"""
        try:
            session = self._tool_to_session[name]
        except KeyError:
            raise ValueError(f"Tool not found: {name}")
        result = await session.call_tool(name, args)
        return "".join(c.text for c in result.content)

    async def cleanup(self) -> None:
        """关闭所有连接"""
        await self._exit_stack.aclose()