import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

from deepagent.agent import get_final_response

async def main():
    queries = [
        "How many users are there?",
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        
        response = await get_final_response(query, "test_ask_endpoint")
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
