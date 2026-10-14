# Agents and Memory

This repository contains a Python personal AI assistant built with LangChain
and LangGraph. It can answer general questions and use tools to manage tasks
and reminders, calculate values, search the web, work with saved memories, and
draft or send email with human approval.

The application code lives in [`Practice/`](./Practice/).

## What it includes

- **Chat interfaces:** an interactive command-line assistant and a FastAPI
  `/chat` endpoint.
- **Local language model:** Ollama with `qwen3:8b` for assistant responses.
- **Task and reminder management:** create, list, update, complete, and delete
  records stored in SQLite.
- **Human approval:** task deletion and email sending pause for approval before
  proceeding.
- **Tools:** arithmetic and percentage calculations, local date/time, web
  search, a demo external user service, email drafting, and memory recall/save.
- **Conversation and memory storage:** a LangGraph checkpointer for conversation
  state and a SQLite-backed semantic memory store using Ollama embeddings.
- **Deployment and evaluation files:** Docker configuration and an optional
  LangSmith evaluation script.

## Repository layout

```text
.
├── README.md
└── Practice/
    ├── app/
    │   ├── agent.py             # Main LangChain agent, prompt, tools, approvals
    │   ├── api.py               # FastAPI chat API (port 8001)
    │   ├── main.py              # Interactive command-line chat
    │   ├── external_service.py  # Small demo FastAPI user service (port 8000)
    │   ├── agentt/              # Intent, extraction, planning, and retry helpers
    │   ├── database/            # SQLite connection and task/reminder schema
    │   ├── memory/              # LangGraph checkpointer and semantic store
    │   ├── middleware/          # Agent guardrails
    │   └── tools/               # Task, reminder, email, search, memory, etc.
    ├── tests/
    │   ├── test_agent.py        # Agent and tool-routing tests
    │   ├── test_tools.py        # Calculator test
    │   └── langsmith_eval.py    # Optional hosted evaluation
    ├── data/                    # SQLite data/checkpoint files
    ├── requirements.txt
    ├── Dockerfile
    ├── compose.yaml
    └── langgraph.json
```

The `agentt/` directory also contains standalone retry and service-check
scripts. The core assistant is assembled in `app/agent.py`; not every helper in
`agentt/` is part of the active request path.

## Requirements

- Python and pip (the Docker image uses Python 3.14).
- [Ollama](https://ollama.com/) running locally, with the models used by the
  project available:

  ```powershell
  ollama pull qwen3:8b
  ollama pull nomic-embed-text
  ```

- Install the packages listed in `Practice/requirements.txt`.
- For email sending, a Microsoft identity application configured for the
  `Mail.Send` scope is also required.

## Set up locally

In PowerShell, from the repository root:

```powershell
cd Practice
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The assistant defaults to Ollama at `http://localhost:11434`. To use another
Ollama URL, set `OLLAMA_BASE_URL` in the environment or in a `Practice/.env`
file. Email authentication reads `CLIENT_ID` and `AUTHORITY` from that file;
these are only needed for email functionality. Do not commit credentials or
private configuration.

## Run the assistant

From the `Practice/` directory with the virtual environment activated:

**Command-line chat**

```powershell
python -m app.main
```

Enter `exit` or `quit` to stop.

**HTTP API**

```powershell
python -m uvicorn app.api:app --reload --port 8001
```

The API documentation is available at `http://localhost:8001/docs`. Send a
chat request to `POST /chat` with a JSON body such as:

```json
{
  "message": "What is 20% of 5000?"
}
```

When an action requires approval, the API responds that it is waiting. Send
`yes` or `no` in a subsequent `/chat` request to resume or cancel that action.

The assistant's external-service tool calls a separate demo service at
`http://127.0.0.1:8000`. To use it, start a second terminal in `Practice/` and
run:

```powershell
python -m uvicorn app.external_service:app --reload --port 8000
```

## Run tests

From `Practice/`:

```powershell
python -m pip install pytest
python -m pytest -q tests/test_tools.py
```

`tests/test_agent.py` invokes the configured Ollama model, so it also requires
Ollama to be running with `qwen3:8b` available:

```powershell
python -m pytest -q tests/test_agent.py
```

## Run with Docker Compose

Docker Compose expects a `Practice/.env` file and an external named Docker
volume. Create the volume once, then start the service from `Practice/`:

```powershell
docker volume create personal-ai-assistant-data
docker compose up --build
```

The API is exposed on port `8001`. Compose configures the container to reach
Ollama on the host at `http://host.docker.internal:11434` and persists
LangGraph checkpoints in the named volume.

## Optional LangSmith evaluation

`tests/langsmith_eval.py` creates and runs the
`personal-assistant-evaluation` dataset. It requires a `LANGSMITH_API_KEY` in
the environment or `Practice/.env`, plus the LangSmith Python package (which
is not listed in `requirements.txt`):

```powershell
python -m pip install langsmith
python tests/langsmith_eval.py
```
