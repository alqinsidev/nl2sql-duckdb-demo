from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from deepagent.core.llm import get_llm
from deepagent.database.connection import get_db_engine
from deepagent.core.logger import logger

@tool
def ask_database(query: str) -> str:
    """
    Useful for answering natural language questions about the e-commerce database 
    (sales, revenues, products, customers, orders, etc).
    Input should be a fully formed question.
    """
    logger.info(f"Executing SQL Agent for query: {query}")
    try:
        engine = get_db_engine()
        db = SQLDatabase(engine)
        llm = get_llm()
        
        # Use "zero-shot-react-description" as string to avoid import issues
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            agent_type="zero-shot-react-description",
            verbose=False,
            handle_parsing_errors=True
        )
        
        result = agent_executor.invoke({"input": query})
        
        # Check if the result is a dict (likely)
        if isinstance(result, dict) and "output" in result:
            return result["output"]
        return str(result)
        
    except Exception as e:
        logger.error(f"Error in ask_database: {e}")
        return f"An error occurred while querying the database: {str(e)}"

tool = ask_database
