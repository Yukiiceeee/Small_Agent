import json
import random

schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的当前天气信息，包括温度、湿度、天气状况和风力。",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "要查询天气的城市名称，例如 '北京'、'上海'、'杭州'"
                }
            },
            "required": ["city"]
        }
    }
}


def execute(args: dict) -> str:
    """模拟天气查询，返回 JSON 格式的天气数据。"""
    city = args.get("city", "未知城市")

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
