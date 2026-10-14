from app.agentt.retry import LLMRetryableError


def classify_llm_error(error: Exception) -> Exception:
    message = str(error).lower()

    retryable_messages = (
        "connection",
        "connect",
        "timeout",
        "timed out",
        "temporarily unavailable",
        "server error",
        "internal server error",
        "service unavailable",
        "rate limit",
        "rate_limit",
        "rate_limit_exceeded",
        "too many requests",
        "429",
        "quota exceeded",
        "tokens per day",
        "tokens per minute",
        "limit exceeded",
        "overloaded",
    )

    if any(
        text in message
        for text in retryable_messages
    ):
        return LLMRetryableError(
            f"LLM temporarily unavailable or rate limited: {error}"
        )

    return error