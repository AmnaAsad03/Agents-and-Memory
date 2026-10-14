from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from app.agent import agent
from app.database.database import initialize_database


app = FastAPI(
    title="Personal AI Assistant",
    description="Agentic AI personal assistant API",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.on_event("startup")
def startup():
    initialize_database()


def get_approval_response(message: str):
    normalized = message.strip().lower()

    approve_phrases = {
        "yes",
        "y",
        "yes send it",
        "yes, send it",
        "send it",
        "go ahead",
        "go ahead and send it",
        "approved",
        "approve",
    }

    reject_phrases = {
        "no",
        "n",
        "no don't send it",
        "no, don't send it",
        "don't send it",
        "do not send it",
        "cancel",
        "cancel it",
        "reject",
    }

    if normalized in approve_phrases:
        return "yes"

    if normalized in reject_phrases:
        return "no"

    return None


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    config: RunnableConfig = {
        "configurable": {
            "thread_id": "personal-assistant",
        }
    }

    message = request.message.strip()

    approval = get_approval_response(message)

    if approval is not None:
        try:
            result = agent.invoke(
                Command(resume=approval),
                config=config,
            )

            print("APPROVAL RESULT:")
            print(result)

            if "__interrupt__" in result:
                return ChatResponse(
                    response="Still waiting for approval."
                )

            last_message = result["messages"][-1]

            return ChatResponse(
                response=last_message.content or "Request completed."
            )

        except Exception as exc:
            print("Approval resume failed:", repr(exc))

            raise HTTPException(
                status_code=500,
                detail=f"Approval resume failed: {exc}",
            )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        config=config,
    )

    print("CHAT RESULT:")
    print(result)

    if "__interrupt__" in result:
        return ChatResponse(
            response="Waiting for your approval."
        )

    last_message = result["messages"][-1]

    return ChatResponse(
        response=last_message.content or "Request completed."
    )