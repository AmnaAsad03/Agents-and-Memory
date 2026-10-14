import os
from dotenv import load_dotenv
from langsmith import Client

from app.agent import agent

load_dotenv()
DATASET_NAME = "personal-assistant-evaluation"


def run_agent(inputs: dict) -> dict:
    user_request = inputs["user_request"]

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_request,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "langsmith-evaluation",
            }
        },
    )

    tool_names = []

    for message in result["messages"]:
        if hasattr(message, "tool_calls"):
            for tool_call in message.tool_calls:
                tool_names.append(tool_call["name"])

    final_message = result["messages"][-1]

    return {
        "response": str(final_message.content),
        "tool_names": tool_names,
    }


def evaluate_agent_output(
    outputs: dict,
    reference_outputs: dict,
) -> dict:
    expected_tool = reference_outputs["expected_tool"]
    expected_result = reference_outputs["expected_result"]

    tool_correct = expected_tool in outputs["tool_names"]
    result_correct = expected_result.lower() in outputs["response"].lower()

    return {
        "key": "agent_correctness",
        "score": int(tool_correct and result_correct),
        "comment": (
            f"Expected tool: {expected_tool}; "
            f"Actual tools: {outputs['tool_names']}; "
            f"Expected result: {expected_result}"
        ),
    }


def create_dataset(client: Client):
    if client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset already exists: {DATASET_NAME}")
        return

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for the Personal AI Assistant.",
    )

    examples = [
        {
            "inputs": {
                "user_request": "What is 20% of 5000?",
            },
            "outputs": {
                "expected_tool": "calculate",
                "expected_result": "1000",
            },
        },
        {
            "inputs": {
                "user_request": "What is 30% of 8000?",
            },
            "outputs": {
                "expected_tool": "calculate",
                "expected_result": "2400",
            },
        },
        {
            "inputs": {
                "user_request": "Calculate 15% of 2000.",
            },
            "outputs": {
                "expected_tool": "calculate",
                "expected_result": "300",
            },
        },
    ]

    client.create_examples(
        dataset_id=dataset.id,
        examples=examples,
    )

    print(f"Created dataset: {dataset.name}")
    print(f"Created {len(examples)} evaluation examples.")


def main():
    if not os.getenv("LANGSMITH_API_KEY"):
        raise RuntimeError(
            "LANGSMITH_API_KEY is not set."
        )

    client = Client()

    create_dataset(client)

    results = client.evaluate(
        run_agent,
        data=DATASET_NAME,
        evaluators=[evaluate_agent_output],
        experiment_prefix="personal-assistant-evaluation",
        description="Evaluate tool selection and final result.",
        max_concurrency=1,
    )

    print("\nLangSmith evaluation completed.")
    print(results)


if __name__ == "__main__":
    main()