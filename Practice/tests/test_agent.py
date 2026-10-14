from app.agent import agent
from app.agentt.clarification_manager import check_request
from app.agent import (
    agent,
    delete_task_with_approval,
    send_email_with_approval,
)
from app.agentt.llm_errors import classify_llm_error
from app.agentt.retry import LLMRetryableError


def test_rate_limit_errors_are_retryable():
    error = ValueError("Rate limit reached for model; 429 Too Many Requests")

    classified = classify_llm_error(error)

    assert isinstance(classified, LLMRetryableError)

def test_agent_selects_calculator():
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 20% of 5000?",
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "evaluation-tool-selection-1",
            }
        },
    )

    tool_calls = []

    for message in result["messages"]:
        if hasattr(message, "tool_calls"):
            tool_calls.extend(message.tool_calls)

    tool_names = [
        tool_call["name"]
        for tool_call in tool_calls
    ]

    assert "calculate" in tool_names


def test_agent_passes_correct_tool_arguments():
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 20% of 5000?",
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "evaluation-tool-arguments-1",
            }
        },
    )

    tool_calls = []

    for message in result["messages"]:
        if hasattr(message, "tool_calls"):
            tool_calls.extend(message.tool_calls)

    calculate_calls = [
        tool_call
        for tool_call in tool_calls
        if tool_call["name"] == "calculate"
    ]

    assert calculate_calls

    arguments = calculate_calls[0]["args"]

    assert arguments["expression"] == "20% of 5000"


def test_agent_completes_calculation():
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 20% of 5000?",
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "evaluation-task-completion-1",
            }
        },
    )

    final_message = result["messages"][-1]
    final_response = str(final_message.content)

    assert "1000" in final_response


def test_agent_response_quality():
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is 20% of 5000?",
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "evaluation-response-quality-1",
            }
        },
    )

    final_message = result["messages"][-1]
    response = str(final_message.content).strip()

    assert response
    assert len(response) > 5
    assert "1000" in response


    
def test_missing_information_detection():
    result = check_request(
        "Create a reminder."
    )

    assert result["intent"] == "create_reminder"
    assert "title" in result["missing_fields"]
    assert "reminder_time" in result["missing_fields"]    
    
    
    
    
def test_delete_task_requires_approval(monkeypatch):
    delete_called = False

    def fake_delete_task(arguments):
        nonlocal delete_called
        delete_called = True

    monkeypatch.setattr(
        "app.agent.interrupt",
        lambda _: "no",
    )

    monkeypatch.setattr(
        "app.agent.delete_task",
        type(
            "MockDeleteTask",
            (),
            {
                "invoke": staticmethod(fake_delete_task),
            },
        )(),
    )

    result = delete_task_with_approval.invoke(
        {
            "task_id": 999,
        }
    )

    assert "cancelled" in result.lower()
    assert delete_called is False


def test_send_email_requires_approval(monkeypatch):
    send_called = False

    def fake_send_email(email):
        nonlocal send_called
        send_called = True

    monkeypatch.setattr(
        "app.agent.interrupt",
        lambda _: "no",
    )

    monkeypatch.setattr(
        "app.agent.send_email",
        fake_send_email,
    )

    result = send_email_with_approval.invoke(
        {
            "email": {
                "recipient": "test@example.com",
                "subject": "Test",
                "body": "Test email",
            }
        }
    )

    assert "cancelled" in result.lower()
    assert send_called is False    