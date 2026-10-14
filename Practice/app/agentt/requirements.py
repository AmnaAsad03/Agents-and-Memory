REQUIRED_FIELDS = {
    "create_reminder": ["title", "reminder_time"],
    "update_reminder": ["reminder_id"],
    "delete_reminder": ["reminder_id"],
    "complete_reminder": ["reminder_id"],
    "view_reminders": [],
    "create_task": ["title"],
    "update_task": ["task_id"],
    "delete_task": ["task_id"],
    "complete_task": ["task_id"],
    "view_tasks": [],
    "calculate": ["calculation"],
    "get_current_datetime": [],
    "normal_question": [],
}


def get_required_fields(intent: str) -> list[str]:
    return REQUIRED_FIELDS.get(intent, [])