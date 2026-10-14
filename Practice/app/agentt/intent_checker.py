import re

from app.agent import model


def _fallback_intent(user_request: str) -> str:
    text = user_request.strip().lower()

    if "reminder" in text and any(word in text for word in ["create", "set", "schedule"]):
        return "create_reminder"
    if "reminder" in text and "update" in text:
        return "update_reminder"
    if "reminder" in text and "delete" in text:
        return "delete_reminder"
    if "reminder" in text and "complete" in text:
        return "complete_reminder"
    if "reminder" in text and "view" in text:
        return "view_reminders"

    if "task" in text and any(word in text for word in ["create", "add", "new"]):
        return "create_task"
    if "task" in text and "update" in text:
        return "update_task"
    if "task" in text and any(word in text for word in ["delete", "remove"]):
        return "delete_task"
    if "task" in text and "complete" in text:
        return "complete_task"
    if "task" in text and any(word in text for word in ["show", "list", "view"]):
        return "view_tasks"

    if re.search(r"\d+(?:\.\d+)?%\s+of\s+\d+(?:\.\d+)?", text):
        return "calculate"
    if any(word in text for word in ["what time", "what is the date", "current date", "current time"]):
        return "get_current_datetime"

    return "normal_question"


def check_intent(user_request: str) -> str:
    try:
        prompt = f"""
Analyze the user's request and identify the intended action.

User request:
{user_request}

Return only one action from this list:
create_reminder
update_reminder
delete_reminder
complete_reminder
view_reminders
create_task
update_task
delete_task
complete_task
view_tasks
calculate
get_current_datetime
normal_question
"""

        response = model.invoke(prompt)
        value = str(response.content).strip()
        if value:
            return value
    except Exception:
        pass

    return _fallback_intent(user_request)


if __name__ == "__main__":
    request = input("Enter request: ")
    intent = check_intent(request)
    print(f"Detected intent: {intent}")