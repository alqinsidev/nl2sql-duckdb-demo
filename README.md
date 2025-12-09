# 🦆 NL2SQL DuckDB Demo

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![DuckDB](https://img.shields.io/badge/DuckDB-Enabled-yellow)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Ready-teal)

> **Chat with your database in plain English.**

This project is a **powerful showcase** of how to build a "Chatbot for your Database" using **LangChain DeepAgent** and **DuckDB**. It comes pre-loaded with a dummy e-commerce dataset, so you can start asking questions immediately—no complex setup required.

> **Note**: This project is based on the [DeepAgent Starter Kit](https://github.com/alqinsidev/deepagent-starter).

<img src="https://github.com/alqinsidev/nl2sql-duckdb-demo/blob/main/doc/unique-user-2024.gif" alt="Demo GIF" width="800"/>

---

## 🚀 Quick Start

Get up and running in less than 2 minutes.

### Prerequisites
- Python 3.10+
- [Docker](https://www.docker.com/) (optional, for containerized run)
- A **Google AI Studio API Key** (for Gemini)

### 1. Installation

Use the included `Makefile` to set up your environment easily:

```bash
# Clone the repository
git clone https://github.com/alqinsidev/nl2sql-duckdb-demo.git
cd nl2sql-duckdb-demo

# Create venv and install dependencies
make install
```

### 2. Configure Credentials

Create your `.env` file:

```bash
cp .env.example .env
```

Open `.env` and paste your API key:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run the Server

```bash
# Start the local server
make run
```

That's it! The API is live at `http://localhost:8000`.

---

## ⚡️ Try These Questions

Once the server is running, use `curl` or your browser to ask questions.

**Simple Aggregations:**
> "How many total users do we have?"
>
> "What is the total sales amount for 2024?"

**Complex Filtering:**
> "List the top 5 most expensive products."
>
> "How many transactions were made by unique users in 2024?"

**Drill-down:**
> "Show me the sales trend for 'Fashion' over the last 3 months."

**Example cURL command:**
```bash
curl -N "http://localhost:8000/chat?q=How%20many%20products%20are%20in%20the%20database?"
```

---

## 📂 What's Inside the Database?

The project includes `ecommerce.duckdb`, a pre-populated OLAP database with the following schema:

| Table | Description |
| :--- | :--- |
| **`dim_product`** | Product catalog (id, name, category, price) |
| **`dim_customer`** | Customer profiles (id, name, email) |
| **`dim_geography`** | Location data for customers/orders |
| **`dim_date`** | Date dimension for temporal analysis |
| **`fact_orders`** | Transactional records linking all dimensions |

---

## 🛠 Features

- **Zero-Setup Database**: Uses DuckDB (in-process SQL OLAP), so there's no need to install PostgreSQL or MySQL.
- **Intelligent Routing**: The agent decides when to consult the database versus general knowledge.
- **Context Aware**: Remembers your previous questions for natural follow-ups.
- **Production Ready**: Built with FastAPI, Pydantic Settings, and Structured Logging.

## 🏗 Architecture

<img width="800" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/7984a651-3916-4a5f-b8bb-7127e7084e5b" />

1.  **User** sends a natural language query.
2.  **DeepAgent** (Orchestrator) analyzes the intent.
3.  If data is needed, it delegates to the **SQL Tool**.
4.  **SQL Agent** generates a DuckDB-compatible SQL query.
5.  **DuckDB** executes the query and returns results.
6.  **DeepAgent** synthesizes the final answer.

---

## 🐳 Docker Support

Prefer Docker? We've got you covered.

```bash
make docker-up
```

---

## ❓ Troubleshooting

**Q: `ModuleNotFoundError` when running python manually?**
A: Make sure your `PYTHONPATH` includes the `src` directory. The `make run` command handles this for you.

**Q: Agent returns "I don't know"?**
A: Ensure your `GOOGLE_API_KEY` is valid. Also, check the console logs—sometimes the LLM generates invalid SQL which the agent catches and retries, but if it fails repeatedly, it may give up.

---

## 🤝 Contributing

This project is a demo, but feel free to open issues or PRs if you want to improve the tooling or add more complex datasets!
