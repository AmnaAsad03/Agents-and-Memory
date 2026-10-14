
from typing import Any

from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage


class GuardrailViolation(Exception):
    """Raised when a request violates a safety policy."""


class GuardrailsMiddleware(AgentMiddleware):
    """Middleware for input, tool, and output safety checks."""

    def before_agent(
        self,
        state,
        runtime,
    ) -> dict[str, Any] | None:

        messages = state.get("messages", [])

        if not messages:
            raise GuardrailViolation(
                "The request cannot be empty."
            )

        user_message = messages[-1]

        content = getattr(
            user_message,
            "content",
            "",
        )

        if not isinstance(content, str):
            return None

        request = content.strip().lower()

        blocked_requests = {
            "delete all my tasks",
            "delete all tasks",
            "remove all my tasks",
            "remove all tasks",
        }

        if request in blocked_requests:
            raise GuardrailViolation(
                "Deleting all tasks is not allowed automatically. "
                "Delete tasks individually with approval."
            )

        return None

    def wrap_tool_call(
        self,
        request: Any,
        handler: Any,
    ) -> Any:

        tool_name = request.tool_call["name"]
        tool_args = request.tool_call.get("args", {})

        if tool_name == "delete_task_with_approval":
            task_id = tool_args.get("task_id")

            if not isinstance(task_id, int) or task_id <= 0:
                return ToolMessage(
                    content=(
                        "Tool blocked: task_id must be a "
                        "positive integer."
                    ),
                    tool_call_id=request.tool_call["id"],
                    status="error",
                )

        if tool_name == "send_email":
            return ToolMessage(
                content=(
                    "Tool blocked: direct email sending is not "
                    "allowed. Human-approved email sending is required."
                ),
                tool_call_id=request.tool_call["id"],
                status="error",
            )

        if tool_name == "send_email_with_approval":
            email = tool_args.get("email")

            if not isinstance(email, dict):
                return ToolMessage(
                    content="Tool blocked: email data is invalid.",
                    tool_call_id=request.tool_call["id"],
                    status="error",
                )

            required_fields = {
                "recipient",
                "subject",
                "body",
            }

            missing_fields = required_fields - set(email.keys())

            if missing_fields:
                return ToolMessage(
                    content=(
                        "Tool blocked: email is missing required "
                        f"fields: {', '.join(sorted(missing_fields))}."
                    ),
                    tool_call_id=request.tool_call["id"],
                    status="error",
                )

        return handler(request)

    async def awrap_tool_call(
        self,
        request: Any,
        handler: Any,
    ) -> Any:

        tool_name = request.tool_call["name"]
        tool_args = request.tool_call.get("args", {})

        if tool_name == "delete_task_with_approval":
            task_id = tool_args.get("task_id")

            if not isinstance(task_id, int) or task_id <= 0:
                return ToolMessage(
                    content=(
                        "Tool blocked: task_id must be a "
                        "positive integer."
                    ),
                    tool_call_id=request.tool_call["id"],
                    status="error",
                )

        if tool_name == "send_email":
            return ToolMessage(
                content=(
                    "Tool blocked: direct email sending is not "
                    "allowed. Human-approved email sending is required."
                ),
                tool_call_id=request.tool_call["id"],
                status="error",
            )

        if tool_name == "send_email_with_approval":
            email = tool_args.get("email")

            if not isinstance(email, dict):
                return ToolMessage(
                    content="Tool blocked: email data is invalid.",
                    tool_call_id=request.tool_call["id"],
                    status="error",
                )

            required_fields = {
                "recipient",
                "subject",
                "body",
            }

            missing_fields = required_fields - set(email.keys())

            if missing_fields:
                return ToolMessage(
                    content=(
                        "Tool blocked: email is missing required "
                        f"fields: {', '.join(sorted(missing_fields))}."
                    ),
                    tool_call_id=request.tool_call["id"],
                    status="error",
                )

        return await handler(request)

    def after_agent(
        self,
        state,
        runtime,
    ) -> dict[str, Any] | None:

        messages = state.get("messages", [])

        if not messages:
            raise GuardrailViolation(
                "The agent produced no response."
            )

        last_message = messages[-1]

        content = getattr(
            last_message,
            "content",
            "",
        )

        if content is None:
            raise GuardrailViolation(
                "The agent produced an empty response."
            )

        if isinstance(content, str) and not content.strip():
            raise GuardrailViolation(
                "The agent produced an empty response."
            )

        return None
