import sys
import os

# Add the src directory to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from deepagent.core.config import settings
from deepagent.core.loader import load_tools
from deepagent.core.logger import logger

def test_config():
    print("Testing Configuration...")
    print(f"Model Name: {settings.MODEL_NAME}")
    print(f"Log Level: {settings.LOG_LEVEL}")
    assert settings.MODEL_NAME is not None
    print("Configuration Test Passed!")

def test_tool_loading():
    print("\nTesting Tool Loading...")
    tools = load_tools()
    print(f"Loaded {len(tools)} tools.")
    for t in tools:
        print(f" - {t.name}: {t.description}")
    
    assert len(tools) >= 2
    print("Tool Loading Test Passed!")

def test_logger():
    print("\nTesting Logger...")
    logger.info("This is a test log message.")
    print("Logger Test Passed!")

if __name__ == "__main__":
    try:
        test_config()
        test_tool_loading()
        test_logger()
        print("\nAll Tests Passed Successfully!")
    except Exception as e:
        print(f"\nTest Failed: {e}")
        sys.exit(1)
