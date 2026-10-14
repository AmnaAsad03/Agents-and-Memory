from ddgs import DDGS


def search_web(query: str):
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            max_results=5,
        )

    return results


if __name__ == "__main__":
    query = "latest Python version"

    results = search_web(query)

    print(f"\nSearch results for: {query}\n")

    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['title']}")
        print(f"   {result['href']}")
        print(f"   {result['body']}\n")