from langfuse.langchain import CallbackHandler
import inspect

print(inspect.signature(CallbackHandler.__init__))
