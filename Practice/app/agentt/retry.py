import time
from typing import Any, Callable


class RetryableError(Exception):
    """Error that may succeed if the operation is tried again."""


class DatabaseRetryableError(RetryableError):
    """Temporary database error that can be retried."""


class LLMRetryableError(RetryableError):
    """Temporary LLM error that can be retried."""


def retry_operation(
    operation: Callable[[], Any],
    max_retries: int = 2,
    backoff_seconds: float = 1.0,
) -> Any:

    attempts = 0

    while True:
        try:
            return operation()

        except RetryableError:
            attempts += 1

            if attempts > max_retries:
                raise

            time.sleep(
                backoff_seconds * attempts
            )

        except Exception:
            raise