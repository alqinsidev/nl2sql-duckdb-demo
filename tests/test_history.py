import sys
import os
import asyncio
import json

# Add the src directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from deepagent.agent import stream_agent_response

async def test_history():
    thread_id = "test_thread_123"
    
    print("--- Turn 1: Setting Name ---")
    response_text = ""
    async for chunk in stream_agent_response("My name is Alice", thread_id=thread_id):
        # sse-starlette yields dicts now with "event" and "data"
        if isinstance(chunk, dict) and chunk.get("event") == "content_block_delta":
            data = json.loads(chunk["data"])
            if "delta" in data and "text" in data["delta"]:
                response_text += data["delta"]["text"]
            
    print(f"Agent: {response_text}")
    
    print("\n--- Turn 2: Asking Name ---")
    response_text = ""
    async for chunk in stream_agent_response("What is my name?", thread_id=thread_id):
        if isinstance(chunk, dict) and chunk.get("event") == "content_block_delta":
            data = json.loads(chunk["data"])
            if "delta" in data and "text" in data["delta"]:
                response_text += data["delta"]["text"]

    print(f"Agent: {response_text}")
    
    if "Alice" in response_text:
        print("\nSUCCESS: Agent remembered the name!")
    else:
        print("\nFAILURE: Agent did not remember the name.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_history())
