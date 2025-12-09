import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from deepagent.agent import graph

async def main():
    queries = [
        "How many users are there?",
        "What is the total revenue by month? Show me the first 3 months."
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        config = {"configurable": {"thread_id": "test_thread"}}
        # We need to collect the final answer
        final_answer = ""
        
        async for event in graph.astream_events(
            {"messages": [("user", query)]},
            version="v1",
            config=config
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                content = chunk.content
                if content:
                    text = ""
                    if isinstance(content, str):
                        text = content
                    elif isinstance(content, list):
                        for c in content:
                            if isinstance(c, str):
                                text += c
                            elif isinstance(c, dict) and 'text' in c:
                                text += c['text']
                    
                    print(text, end="", flush=True)
                    final_answer += text
            elif kind == "on_tool_start":
                print(f"\n[Tool Call: {event['name']}]")
        
        print("\n" + "-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
