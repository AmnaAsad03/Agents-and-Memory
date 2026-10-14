from dotenv import load_dotenv

load_dotenv()

from app.agent import agent
from app.database.database import initialize_database


def main():
    initialize_database()

    print("Personal AI Assistant")
    print("Type 'exit' or 'quit' to stop.")

    conversation_history = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            break

        if not user_input:
            continue

        result = agent.invoke(
            {
                "messages": conversation_history
                + [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            },
            config={
                "configurable": {
                    "thread_id": "personal-assistant",
                }
            },
        )

        conversation_history = result["messages"]

        print(
            f"\nAssistant: "
            f"{result['messages'][-1].content}"
        )


if __name__ == "__main__":
    main()