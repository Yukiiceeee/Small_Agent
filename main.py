import asyncio
from src.agent import Agent
from src.client import OpenAIClient
# from tools import TOOL_MAP, TOOL_SCHEMAS
from prompt import SYS_PROMPT, REACT_SYS_PROMPT
from configs.config import load_config, load_mcp_config
from src.workflows.base import BaseWorkflow
from src.workflows.simple_loop import SimpleWorkflow
from src.workflows.react import ReActWorkflow
from src.workflows.reflection import ReflectionWorkflow
from src.workflows.plan_execute import PlanExecuteWorkflow
from src.mcp_client import MCPManager

WORKFLOW_REGISTRY = {
      "simple": (SimpleWorkflow, SYS_PROMPT),
      "react": (ReActWorkflow, REACT_SYS_PROMPT),
      "reflection": (ReflectionWorkflow, SYS_PROMPT),
      "plan_execute": (PlanExecuteWorkflow, SYS_PROMPT),
  }

async def main():
    llm_config, agent_config, workflow_config = load_config()

    if llm_config.client.lower() == "openai":
        client = OpenAIClient(
            llm_config
        )
    elif llm_config.client.lower() == "anthropic":
        from .src.client import AnthropicClient
        client = AnthropicClient(
            llm_config
        )
    else:
        raise ValueError(f"不支持的LLM客户端: {llm_config.client}")
    
    mcp_manager = MCPManager()
    server_configs = load_mcp_config()
    await mcp_manager.connect(server_configs)
    
    workflow_cls, sys_prompt = WORKFLOW_REGISTRY[workflow_config.type]
    workflow = workflow_cls(client=client, max_turns=agent_config.max_turns, mcp_manager=mcp_manager)
    agent = Agent(name=agent_config.name, sys_prompt=sys_prompt, workflow=workflow)
    try:
      await agent.run()
    finally:
      await mcp_manager.cleanup()

if __name__ == '__main__':
    asyncio.run(main())