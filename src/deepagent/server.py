from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from .agent import stream_agent_response, get_final_response
from .core.config import settings
from .core.logger import logger
import uvicorn

app = FastAPI(title="DeepAgent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "LangChain DeepAgent with Vertex AI & Langfuse"}

@app.get("/chat")
async def chat(q: str, thread_id: str = "default"):
    logger.info(f"Chat endpoint called with query: {q} (thread_id: {thread_id})")
    return EventSourceResponse(stream_agent_response(q, thread_id))

@app.get("/ask")
async def ask(q: str, thread_id: str = "default"):
    """
    Returns only the final answer as JSON.
    """
    logger.info(f"Ask endpoint called with query: {q} (thread_id: {thread_id})")
    return await get_final_response(q, thread_id)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
