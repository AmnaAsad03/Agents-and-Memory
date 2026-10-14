import requests
from langchain_core.tools import tool


@tool
def get_user_from_service(name: str) -> str:
    """Get user information from the external FastAPI service."""
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/user/{name}",
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        return (
            f"Name: {data['name']}\n"
            f"Role: {data['role']}\n"
            f"Status: {data['status']}"
        )

    except requests.RequestException as error:
        return f"External service error: {error}"