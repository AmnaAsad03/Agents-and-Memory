from langchain_core.tools import tool

from app.memory.store import (
    save_memory,
    get_memory,
    search_memories,
)


@tool
def remember_memory(key: str, value: str) -> str:
    """Remember useful information about the user for future conversations."""
    namespace = ("user", "memory")

    save_memory(
        namespace,
        key,
        {"value": value},
    )

    return f"Memory saved: {key} = {value}"


@tool
def recall_memory(query: str) -> str:
    """Search the user's stored memories using a natural language query."""
    namespace = ("user", "memory")

    memories = search_memories(
        namespace,
        query,
    )

    if not memories:
        return "No relevant memory found."

    results = []

    for memory in memories:
        results.append(
            f"{memory['key']} = {memory['value']['value']}"
        )

    return "Relevant memories:\n" + "\n".join(results)