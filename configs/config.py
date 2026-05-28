import os
import dotenv
from dataclasses import dataclass, field
import yaml

dotenv.load_dotenv()

@dataclass
class LLMConfig:
    client: str = field(default_factory=lambda: os.getenv("CLIENT_TYPE"))
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    base_url: str = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL"))
    model: str = field(default_factory=lambda: os.getenv("DEFAULT_LLM_MODEL"))
    temperature: float = 0.7
    max_tokens: int = 2048

@dataclass
class AgentConfig:
    name: str = "小助手"
    max_turns: int = 10

class WorkflowConfig:
    type: str = "simple"  # simple, react, reflection, plan_execute

def load_config():
    llm_config = LLMConfig()
    agent_config = AgentConfig()
    workflow_config = WorkflowConfig()
    return llm_config, agent_config, workflow_config

def load_mcp_config() -> list[dict]:
      config_path = os.path.join(os.path.dirname(__file__), "mcp_servers.yaml")
      with open(config_path, "r") as f:
          config = yaml.safe_load(f)
      return config.get("mcp_servers", [])
