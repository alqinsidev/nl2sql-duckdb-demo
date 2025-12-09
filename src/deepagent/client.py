import requests
import json
import sys

def chat_with_agent(query):
    url = "http://localhost:8000/chat"
    params = {"q": query}
    
    print(f"User: {query}")
    print("Agent: ", end="", flush=True)
    
    try:
        with requests.get(url, params=params, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:]
                        if data == "[DONE]":
                            break
                        if data.startswith("[Tool Call:"):
                            # Optional: Print tool calls differently or ignore
                            # print(f"\n{data}\n", end="", flush=True)
                            continue
                        
                        # Unescape newlines
                        clean_text = data.replace("\\n", "\n")
                        print(clean_text, end="", flush=True)
            print() # Newline at end
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Plan my day for coding"
    chat_with_agent(query)
