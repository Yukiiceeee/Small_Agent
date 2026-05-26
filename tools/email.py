import json

schema = {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "发送一封电子邮件到指定收件人。用于需要通过邮件通知或传递信息的场景。",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "收件人邮箱地址，例如 'user@example.com'"
                },
                "subject": {
                    "type": "string",
                    "description": "邮件主题"
                },
                "body": {
                    "type": "string",
                    "description": "邮件正文内容"
                }
            },
            "required": ["to", "subject", "body"]
        }
    }
}


def execute(args: dict) -> str:
    """模拟发送邮件，返回发送结果。"""
    to = args.get("to", "")
    subject = args.get("subject", "")
    body = args.get("body", "")

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
