from app.agentt.retry import retry_operation, RetryableError


attempts = 0


def database_operation():
    global attempts

    attempts += 1

    print(f"Database attempt {attempts}")

    if attempts < 3:
        raise RetryableError("Temporary database connection failure")

    return "Database operation succeeded"


result = retry_operation(
    database_operation,
    max_retries=2,
)

print(result)