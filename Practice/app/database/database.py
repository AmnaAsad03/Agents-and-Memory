import sqlite3
from pathlib import Path
from typing import Callable, Any

from app.agentt.database_errors import classify_database_error
from app.agentt.retry import retry_operation


DATABASE_PATH = Path(__file__).resolve().parent / "assistant.db"


def get_connection():
    return sqlite3.connect(
        DATABASE_PATH,
        timeout=1,
    )


def execute_with_retry(
    operation: Callable[[], Any],
    max_retries: int = 2,
) -> Any:

    def database_operation():
        try:
            return operation()

        except Exception as error:
            classified_error = classify_database_error(error)

            if classified_error is not error:
                raise classified_error

            raise

    return retry_operation(
        database_operation,
        max_retries=max_retries,
    )


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )
    """)

    connection.commit()
    connection.close()