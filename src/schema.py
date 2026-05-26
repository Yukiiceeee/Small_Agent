from dataclasses import dataclass, field

@dataclass
class ToolCall:
    id: str
    name: str
    args: dict = field(default_factory=dict)

@dataclass
class ChatResult:
    content: str | None = None
    finish_reason: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)

    def has_tool_calls(self):
        return len(self.tool_calls) > 0



