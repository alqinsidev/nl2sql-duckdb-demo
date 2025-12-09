import sys
import os
import asyncio

# Add the src directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from deepagent.core.http_client import safe_request
from deepagent.tools.example_http import get_random_joke

def test_safe_request():
    print("Testing safe_request...")
    url = "https://official-joke-api.appspot.com/random_joke"
    data = safe_request("GET", url)
    
    if data and "setup" in data and "punchline" in data:
        print("SUCCESS: safe_request returned valid data.")
        print(f"Joke: {data['setup']} - {data['punchline']}")
    else:
        print(f"FAILURE: safe_request returned invalid data: {data}")
        sys.exit(1)

def test_tool_execution():
    print("\nTesting get_random_joke tool...")
    result = get_random_joke.invoke({})
    
    if result and "Sorry" not in result:
        print("SUCCESS: Tool executed successfully.")
        print(f"Result: {result}")
    else:
        print(f"FAILURE: Tool execution failed: {result}")
        sys.exit(1)

if __name__ == "__main__":
    test_safe_request()
    test_tool_execution()
