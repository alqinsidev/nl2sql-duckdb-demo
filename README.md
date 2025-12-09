# LangChain DeepAgent

A production-ready LangChain agent with HTTP tools, Gemini API, Langfuse integration, and conversation history support.

## Features

- **Dynamic Tool Loading**: Automatically loads tools from `src/deepagent/tools`.
- **Conversation History**: Remembers context across turns using `thread_id`.
- **Structured Logging**: JSON-formatted logs for production.
- **Configuration Management**: Robust configuration using `pydantic-settings`.
- **Docker Support**: Ready for containerized deployment.
- **SSE Streaming**: Real-time response streaming.

## Project Structure

```
.
├── src/
│   └── deepagent/
│       ├── __init__.py
│       ├── main.py       # Entry point
│       ├── server.py     # FastAPI server
│       ├── agent.py      # Agent logic
│       ├── core/         # Core infrastructure (config, logger, loader)
│       └── tools/        # Tool definitions
├── tests/                # Verification scripts
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Setup

1.  **Create Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in the values:
    ```bash
    cp .env.example .env
    ```
    - `GOOGLE_API_KEY`: Your Google AI Studio API Key.
    - `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`: Your Langfuse credentials.

## Running Locally

Run the server using the module path:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python -m deepagent.main
```

## Running with Docker

1.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

The API will be available at `http://localhost:8000`.

## Usage

### Chat with History
Pass a `thread_id` to maintain conversation context.

**Turn 1:**
```bash
curl -N "http://localhost:8000/chat?q=My%20name%20is%20Alice&thread_id=session1"
```

**Turn 2:**
```bash
curl -N "http://localhost:8000/chat?q=What%20is%20my%20name?&thread_id=session1"
```

### Adding New Tools
1. Create a new file in `src/deepagent/tools/` (e.g., `my_tool.py`).
2. Define your tool using the `@tool` decorator.
3. Export the tool variable as `tool`.

```python
from langchain.tools import tool

@tool
def my_tool(arg: str) -> str:
    """Description."""
    return "result"

tool = my_tool
```
The agent will automatically pick it up on restart.
