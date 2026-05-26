from src.agent import Agent
from src.client import OpenAIClient
from tools import TOOL_MAP, TOOL_SCHEMAS
from prompt import SYS_PROMPT
from configs.config import load_config
from src.workflows.base import BaseWorkflow

def main():
    llm_config, agent_config, workflow_config = load_config()

    if llm_config.client.lower() == "openai":
        client = OpenAIClient(
            llm_config
        )
    elif llm_config.client.lower() == "anthropic":
        from src.client import AnthropicClient
        client = AnthropicClient(
            llm_config
        )
    else:
        raise ValueError(f"不支持的LLM客户端: {llm_config.client}")
    
    if workflow_config.type == "simple":
        from src.workflows.simple_loop import SimpleWorkflow
        workflow = SimpleWorkflow(
            client=client,
            tool_schemas=TOOL_SCHEMAS,
            tool_map=TOOL_MAP,
            max_turns=agent_config.max_turns,
        )

        agent = Agent(
        name=agent_config.name,
        sys_prompt=SYS_PROMPT,
        workflow=workflow,
    )
    elif workflow_config.type == "react":
        from src.workflows.react import ReActWorkflow
        workflow = ReActWorkflow(
            client=client,
            tool_schemas=TOOL_SCHEMAS,
            tool_map=TOOL_MAP,
            max_turns=agent_config.max_turns,
        )

        agent = Agent(
        name=agent_config.name,
        sys_prompt=SYS_PROMPT,
        workflow=workflow,
    )
    else:
        raise ValueError(f"不支持的工作流类型: {workflow_config.type}")

    agent.run()

if __name__ == '__main__':
    main()