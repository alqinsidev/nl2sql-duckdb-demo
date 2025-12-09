import os
import time
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from deepagents import create_deep_agent
from langfuse.langchain import CallbackHandler
from langfuse import observe
from langgraph.checkpoint.memory import MemorySaver
from .core.config import settings
from .core.logger import logger
from .core.loader import load_tools

# Initialize Langfuse Callback
langfuse_handler = None
if settings.LANGFUSE_PUBLIC_KEY and settings.LANGFUSE_SECRET_KEY:
    os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_BASE_URL"] = settings.LANGFUSE_BASE_URL or "https://cloud.langfuse.com"

    langfuse_handler = CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY
    )
    logger.info("Langfuse integration enabled.")
else:
    logger.warning("Langfuse credentials not found. Tracing disabled.")

from .core.llm import get_llm

# Initialize Gemini Model
llm = get_llm()

# Define Tools
# Dynamically load tools from the 'tools' package
tools = load_tools()
logger.info(f"Initialized agent with {len(tools)} tools")

# Initialize Memory
memory = MemorySaver()

# Create Deep Agent
# create_deep_agent returns a compiled LangGraph graph
graph = create_deep_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful Deep Agent. You must use your tools to answer questions. If the user asks about data, sales, products, or customers, use the ask_database tool.",
    checkpointer=memory
)

@observe(capture_output=False)
async def stream_agent_response(input_text: str, thread_id: str = "default"):
    """
    Generates a stream of responses from the agent using astream_events for token streaming.
    """
    # DeepAgents expects a dictionary with "messages" or just a list of messages
    # It handles the internal state (plan, file_system, etc.) automatically
    
    logger.info(f"Processing request: {input_text} (thread_id: {thread_id})")
    
    callbacks = []
    if langfuse_handler:
        callbacks.append(langfuse_handler)
        
    config = {"configurable": {"thread_id": thread_id}, "callbacks": callbacks}
    
    # 1. Start Event
    yield {
        "event": "start",
        "data": json.dumps({"status": "started", "timestamp": time.time()})
    }
    
    async for event in graph.astream_events(
        {"messages": [("user", input_text)]},
        version="v1",
        config=config
    ):
        kind = event["event"]
        
        # 2. Message Event (LLM Tokens)
        if kind == "on_chat_model_stream":
            # Filter specific events to avoid streaming Tool calls / Thoughts from internal nodes
            if event.get("metadata", {}).get("langgraph_node") != "model":
                continue
                
            chunk = event["data"]["chunk"]
            content = chunk.content
            if content:
                text_content = ""
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and "text" in item:
                            text_content += item["text"]
                        elif isinstance(item, str):
                            text_content += item
                        else:
                            text_content += str(item)
                elif isinstance(content, dict) and "text" in content:
                    text_content = content["text"]
                else:
                    text_content = str(content)
                
                if text_content:
                    yield {
                        "event": "message",
                        "data": json.dumps({"chunk": text_content})
                    }

    # 5. Stop Event
    yield {
        "event": "stop",
        "data": json.dumps({"status": "completed", "timestamp": time.time()})
    }

@observe(capture_output=False)
async def get_final_response(input_text: str, thread_id: str = "default") -> dict:
    """
    Executes the agent and returns a single JSON object with the final answer.
    """
    logger.info(f"Processing request (final response only): {input_text} (thread_id: {thread_id})")
    
    callbacks = []
    if langfuse_handler:
        callbacks.append(langfuse_handler)
        
    config = {"configurable": {"thread_id": thread_id}, "callbacks": callbacks}
    
    # Use ainvoke to get the final state
    result = await graph.ainvoke(
        {"messages": [("user", input_text)]},
        config=config
    )
    
    messages = result.get("messages", [])
    if messages:
        last_msg = messages[-1]
        # Ensure we return a string
        content = last_msg.content
        if isinstance(content, list):
             # Handle list content (e.g. from Anthropic/Gemini sometimes)
             text_content = ""
             for item in content:
                 if isinstance(item, str):
                     text_content += item
                 elif isinstance(item, dict) and "text" in item:
                     text_content += item["text"]
             return {"answer": text_content}
        return {"answer": str(content)}
        
    return {"answer": "No response generated."}
