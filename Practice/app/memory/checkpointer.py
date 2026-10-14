import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver


CHECKPOINT_DB = os.environ.get("LANGGRAPH_CHECKPOINT_DB", ":memory:")


def create_checkpointer():
    connection = sqlite3.connect(
        CHECKPOINT_DB,
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(connection)

    checkpointer.setup()

    return checkpointer