import sqlite3

from app.agentt.retry import DatabaseRetryableError


def classify_database_error(error: Exception) -> Exception:
    if isinstance(error, sqlite3.OperationalError):
        message = str(error).lower()

        if "locked" in message:
            return DatabaseRetryableError(
                "Database is temporarily locked."
            )

    return error