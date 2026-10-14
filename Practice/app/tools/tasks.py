from langchain_core.tools import tool

from app.database.database import (
    get_connection,
    execute_with_retry,
)


@tool
def create_task(
    title: str,
    description: str = "",
    due_date: str = "",
) -> str:
    """Create a new task with a title, optional description, and optional due date."""

    def database_operation():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, status)
            VALUES (?, ?, ?, ?)
            """,
            (title, description, due_date, "pending"),
        )

        task_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return task_id

    task_id = execute_with_retry(database_operation)

    return f"Task created successfully. Task ID: {task_id}"


@tool
def view_tasks() -> str:
    """View all of the user's tasks.

    Use this when the user asks to see, list, show, check,
    review, or know what tasks they have.
    Always return every task from the database.
    """

    def database_operation():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, title, description, due_date, status
            FROM tasks
            ORDER BY id
            """
        )

        tasks = cursor.fetchall()
        connection.close()

        return tasks

    tasks = execute_with_retry(database_operation)

    if not tasks:
        return "No tasks found."

    return "\n".join(
        f"Task {task[0]}: {task[1]}"
        for task in tasks
    )


@tool
def update_task(
    task_id: int,
    title: str = "",
    description: str = "",
    due_date: str = "",
    status: str = "",
) -> str:
    """Update an existing task. Use this when the user wants to change a task's title, description, due date, or status."""

    def database_operation():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,),
        )

        task = cursor.fetchone()

        if not task:
            connection.close()
            return "NOT_FOUND"

        updates = []
        values = []

        if title:
            updates.append("title = ?")
            values.append(title)

        if description:
            updates.append("description = ?")
            values.append(description)

        if due_date:
            updates.append("due_date = ?")
            values.append(due_date)

        if status:
            updates.append("status = ?")
            values.append(status)

        if not updates:
            connection.close()
            return "NO_CHANGES"

        values.append(task_id)

        cursor.execute(
            f"""
            UPDATE tasks
            SET {", ".join(updates)}
            WHERE id = ?
            """,
            values,
        )

        connection.commit()
        connection.close()

        return "UPDATED"

    result = execute_with_retry(database_operation)

    if result == "NOT_FOUND":
        return f"Task {task_id} not found."

    if result == "NO_CHANGES":
        return "No changes were provided."

    return f"Task {task_id} updated successfully."


@tool
def delete_task(task_id: int) -> str:
    """Delete an existing task by its ID."""

    def database_operation():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,),
        )

        task = cursor.fetchone()

        if not task:
            connection.close()
            return False

        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

        connection.commit()
        connection.close()

        return True

    deleted = execute_with_retry(database_operation)

    if not deleted:
        return f"Task {task_id} not found."

    return f"Task {task_id} deleted successfully."


@tool
def complete_task(task_id: int) -> str:
    """Mark an existing task as completed."""

    def database_operation():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT id FROM tasks WHERE id = ?",
            (task_id,),
        )

        task = cursor.fetchone()

        if not task:
            connection.close()
            return False

        cursor.execute(
            """
            UPDATE tasks
            SET status = ?
            WHERE id = ?
            """,
            ("completed", task_id),
        )

        connection.commit()
        connection.close()

        return True

    completed = execute_with_retry(database_operation)

    if not completed:
        return f"Task {task_id} not found."

    return f"Task {task_id} marked as completed."