from typing import Any, TypedDict


class AgentState(TypedDict):

    messages: list[Any]

    user_request: str

    tool_calls: list[Any]

    tool_results: list[Any]

    current_action: str

    pending_action: dict[str, Any]

    plan: list[str]

    todos: list[dict[str, str]]

    execution_id: str

    execution_status: str

    final_response: str