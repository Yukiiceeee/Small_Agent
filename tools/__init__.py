from tools.weather import schema as weather_schema, execute as weather_execute
from tools.email import schema as email_schema, execute as email_execute

TOOL_MAP = {
    "get_weather": weather_execute,
    "send_email": email_execute,
}

TOOL_SCHEMAS = [weather_schema, email_schema]
