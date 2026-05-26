import json

schema = {
      "type": "function",
      "function": {
          "name": "create_plan",
          "description": "为完成用户的请求制定一个分步骤的执行计划",
          "parameters": {
              "type": "object",
              "properties": {
                  "steps": {
                      "type": "array",
                      "items": {"type": "string"},
                      "description": "按顺序排列的执行步骤列表"
                  },
                  "goal": {
                      "type": "string",
                      "description": "用户的最终目标"
                  }
              },
              "required": ["steps", "goal"]
          }
      }
  }

def execute(args: dict) -> str:
    return json.dumps(args, ensure_ascii=False)