from typing import Any


def create_plan(steps: list[str]) -> list[str]:
    """Create an execution plan from a list of steps."""

    return steps.copy()


def create_todos(plan: list[str]) -> list[dict[str, Any]]:
    """Create todo items from a plan."""

    return [
        {
            "task": step,
            "status": "pending",
        }
        for step in plan
    ]


def update_todo(
    todos: list[dict[str, Any]],
    task: str,
    status: str,
) -> list[dict[str, Any]]:
    """Update the status of a todo item."""

    for todo in todos:
        if todo["task"] == task:
            todo["status"] = status
            break

    return todos


def start_next_todo(
    todos: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], str | None]:
    """Mark the next pending todo as in progress."""

    for todo in todos:
        if todo["status"] == "pending":
            todo["status"] = "in_progress"
            return todos, todo["task"]

    return todos, None


def complete_todo(
    todos: list[dict[str, Any]],
    task: str,
) -> list[dict[str, Any]]:
    """Mark a todo as completed."""

    return update_todo(
        todos,
        task,
        "completed",
    )


def set_execution_status(
    status: str,
) -> str:
    """Set the status of a long-running execution."""

    valid_statuses = {
        "pending",
        "running",
        "waiting_for_approval",
        "waiting_for_information",
        "completed",
        "failed",
    }

    if status not in valid_statuses:
        raise ValueError(
            f"Invalid execution status: {status}"
        )

    return status


def create_execution_plan(user_request: str) -> list[str]:
    """Create a simple execution plan from the user's request."""

    request = user_request.lower()

    if "email" in request and (
        "calculate" in request
        or "%" in request
    ):
        return [
            "Calculate the required value",
            "Draft the email",
            "Send the email after approval",
        ]

    if "email" in request:
        return [
            "Draft the email",
            "Send the email after approval",
        ]

    if (
        "task" in request
        and (
            "calculate" in request
            or "%" in request
        )
    ):
        return [
            "Calculate the required value",
            "Create the task using the calculated value",
        ]

    if "task" in request:
        return [
            "Process the task request",
        ]

    if "reminder" in request:
        return [
            "Process the reminder request",
        ]

    return [
        "Process the user request",
    ]