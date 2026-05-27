import json
from mcp.server.fastmcp import FastMCP
import random

mcp = FastMCP()

@mcp.tool()
def get_weather(city: str) -> str:
    """天气查询，返回 JSON 格式的天气数据。"""
    city = city.strip()

    # 模拟数据，实际项目中替换为真实 API 调用
    mock_data = {
        "北京": {"temp": 28, "humidity": 45, "condition": "晴", "wind": "北风3级"},
        "上海": {"temp": 31, "humidity": 72, "condition": "多云", "wind": "东南风2级"},
        "杭州": {"temp": 33, "humidity": 68, "condition": "阴", "wind": "南风2级"},
        "广州": {"temp": 35, "humidity": 80, "condition": "雷阵雨", "wind": "西南风4级"},
        "深圳": {"temp": 34, "humidity": 78, "condition": "多云转晴", "wind": "南风3级"},
    }

    if city in mock_data:
        weather = mock_data[city]
    else:
        weather = {
            "temp": random.randint(15, 38),
            "humidity": random.randint(30, 90),
            "condition": random.choice(["晴", "多云", "阴", "小雨"]),
            "wind": random.choice(["北风2级", "南风3级", "东风1级"]),
        }

    result = {
        "city": city,
        "temperature": f"{weather['temp']}°C",
        "humidity": f"{weather['humidity']}%",
        "condition": weather["condition"],
        "wind": weather["wind"],
    }
    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """模拟发送邮件，返回发送结果。"""
    to = to.strip()
    subject = subject.strip()
    body = body.strip()

    if not to or "@" not in to:
        return json.dumps({"success": False, "error": "无效的邮箱地址"}, ensure_ascii=False)

    if not subject:
        return json.dumps({"success": False, "error": "邮件主题不能为空"}, ensure_ascii=False)

    # 模拟发送，实际项目中替换为 SMTP 调用
    result = {
        "success": True,
        "message": f"邮件已成功发送至 {to}",
        "details": {
            "to": to,
            "subject": subject,
            "body_preview": body[:50] + "..." if len(body) > 50 else body,
        }
    }
    return json.dumps(result, ensure_ascii=False)

if __name__ == "__main__":
    mcp.run()

