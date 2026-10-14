import sqlite3

from langchain_ollama import OllamaEmbeddings
from langgraph.store.sqlite import SqliteStore


STORE_DB = "data/memory.sqlite"


embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)


connection = sqlite3.connect(
    STORE_DB,
    check_same_thread=False,
    isolation_level=None,
)


store = SqliteStore(
    connection,
    index={
        "dims": 768,
        "embed": embeddings,
        "fields": ["value"],
    },
)

store.setup()


def save_memory(namespace: tuple, key: str, value: dict):
    store.put(
        namespace,
        key,
        value,
        index=["value"],
    )


def get_memory(namespace: tuple, key: str):
    memory = store.get(namespace, key)

    if memory is None:
        return None

    return memory.value


def search_memories(namespace: tuple, query: str):
    memories = store.search(
        namespace,
        query=query,
        limit=5,
    )

    return [
        {
            "key": memory.key,
            "value": memory.value,
        }
        for memory in memories
    ]