import json
import re

from app.agent import model


def _fallback_extract_data(user_request: str, intent: str) -> dict:
    text = user_request.strip()

    if intent == "calculate":
        match = re.search(r"(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if match:
            return {"calculation": f"{match.group(1)}% of {match.group(2)}"}
        return {"calculation": text}

    if intent == "create_reminder":
        return {"title": "", "reminder_time": ""}
    if intent in {"delete_reminder", "complete_reminder"}:
        return {"reminder_id": ""}
    if intent == "create_task":
        return {"title": ""}
    if intent in {"delete_task", "complete_task"}:
        return {"task_id": ""}

    return {}


def extract_data(user_request: str, intent: str) -> dict:
    if intent == "calculate":
        return {"calculation": user_request.strip()}

    try:
        prompt = f"""
Extract the information provided by the user.

Intent:
{intent}

User request:
{user_request}

Return only a valid JSON object.

For create_reminder:
{{
    "title": "",
    "reminder_time": ""
}}

For delete_reminder or complete_reminder:
{{
    "reminder_id": ""
}}

For create_task:
{{
    "title": ""
}}

For delete_task or complete_task:
{{
    "task_id": ""
}}

If information is not provided, use an empty string.
"""

        response = model.invoke(prompt)
        content = str(response.content).strip()
        return json.loads(content)
    except Exception:
        return _fallback_extract_data(user_request, intent)


if __name__ == "__main__":
    request = input("Enter request: ")
    intent = input("Enter intent: ")

    data = extract_data(request, intent)

    print(f"Extracted data: {data}")