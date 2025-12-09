# NL2SQL DuckDB Demo Showcase

A showcase project that leverages **LangChain DeepAgent** and **LangChain SQL Agent** to create a "Chatbot for your Database". This demo integrates [DuckDB](https://duckdb.org/) and comes **pre-loaded with a dummy e-commerce dataset**, allowing users to immediately ask natural language questions about the data without any setup.

> **Note**: This project is based on the [DeepAgent Starter Kit](https://github.com/alqinsidev/deepagent-starter).

## Features

- **Natural Language to SQL**: Automatically converts user questions into executed SQL queries.
- **DuckDB Integration**: High-performance in-process SQL OLAP database integration.
- **Agent Orchestration**: Combines DeepAgent for conversation flow and SQL Agent for database interaction.
- **Conversation History**: Maintains context across turns (e.g., "Show me top products" -> "What about their prices?").
- **Dynamic Tool Loading**: Modular tool system in `src/deepagent/tools`.
- **Ready-to-Use Dummy Data**: Includes `ecommerce.duckdb` populated with sample e-commerce data (sales, products, customers) for immediate testing.
- **Production Ready**: Features structured logging, `pydantic-settings`, and Docker support.

## Architecture


## Project Structure

```
.
├── src/
│   └── deepagent/
│       ├── __init__.py
│       ├── main.py       # Entry point
│       ├── server.py     # FastAPI server
│       ├── agent.py      # Agent orchestration
│       ├── core/         # Core infrastructure (config, logger, loader)
│       └── tools/        # Tools (including sql_tool.py)
├── tests/                # Verification scripts

├── ecommerce.duckdb      # Pre-loaded OLAP database
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

### Chat with Your Database
Pass a `thread_id` to maintain conversation context.

**Example 1: General Question**
```bash
curl -N "http://localhost:8000/chat?q=How%20many%20products%20are%20in%20the%20database?&thread_id=session1"
```

**Example 2: Follow-up**
```bash
curl -N "http://localhost:8000/chat?q=Which%20one%20is%20the%20most%20expensive?&thread_id=session1"
```

### Extending Capabilities
To add more tools, create a new file in `src/deepagent/tools/`. The agent will automatically pick it up.

```python
from langchain.tools import tool

@tool
def my_custom_tool(query: str) -> str:
    """Description of what this tool does."""
    return "result"

tool = my_custom_tool
```
