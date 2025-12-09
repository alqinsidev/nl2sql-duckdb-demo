import os
import warnings
from sqlalchemy import create_engine
from duckdb_engine import DuckDBEngineWarning
from deepagent.core.logger import logger

DB_FILE = "ecommerce.duckdb"

def get_db_engine():
    """
    Creates and returns a SQLAlchemy engine for DuckDB.
    """
    # Suppress DuckDBEngineWarning: duckdb-engine doesn't yet support reflection on indices
    warnings.filterwarnings("ignore", category=DuckDBEngineWarning)

    # Use absolute path for reliability
    db_path = os.path.abspath(DB_FILE)
    connection_string = f"duckdb:///{db_path}"
    
    logger.info(f"Connecting to DuckDB at: {db_path}")
    engine = create_engine(connection_string)
    return engine
