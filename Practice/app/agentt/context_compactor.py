from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama


MAX_MESSAGES = 12
RECENT_MESSAGES_TO_KEEP = 6


llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    reasoning=False,
)


def should_compact(
    messages: list[Any],
    max_messages: int = MAX_MESSAGES,
) -> bool:
    """Check whether conversation history is large enough to compact."""

    return len(messages) > max_messages


def create_compaction_summary(messages: list[Any]) -> str:
    """Use the LLM to summarize older conversation messages."""

    conversation = []

    for message in messages:
        if isinstance(message, HumanMessage):
            conversation.append(
                f"User: {message.content}"
            )

        elif hasattr(message, "content"):
            conversation.append(
                f"Assistant: {message.content}"
            )

    prompt = (
        "Summarize the following conversation for future use by an AI "
        "assistant.\n\n"
        "Keep only important information such as:\n"
        "- user requests\n"
        "- decisions\n"
        "- completed actions\n"
        "- important values\n"
        "- important context\n"
        "- unresolved requests\n\n"
        "Do not add information that is not present.\n"
        "Keep the summary concise.\n\n"
        "Conversation:\n"
        + "\n".join(conversation)
    )

    response = llm.invoke(prompt)

    return response.content


def compact_messages(
    messages: list[Any],
    max_messages: int = MAX_MESSAGES,
    recent_messages_to_keep: int = RECENT_MESSAGES_TO_KEEP,
) -> list[Any]:
    """Replace older messages with an LLM-generated summary."""

    if not should_compact(messages, max_messages):
        return messages

    old_messages = messages[:-recent_messages_to_keep]
    recent_messages = messages[-recent_messages_to_keep:]

    summary = create_compaction_summary(old_messages)

    compacted_messages = [
        SystemMessage(
            content=(
                "Conversation summary from earlier messages:\n"
                f"{summary}"
            )
        )
    ]

    compacted_messages.extend(recent_messages)

    return compacted_messages