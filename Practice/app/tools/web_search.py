from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search the web for current or up-to-date information."""

    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=5,
        )

    if not results:
        return "No search results found."

    formatted_results = []

    for index, result in enumerate(results, start=1):
        formatted_results.append(
            f"{index}. {result['title']}\n"
            f"URL: {result['href']}\n"
            f"Summary: {result['body']}"
        )

    return "\n\n".join(formatted_results)