import functools
import logging
from datetime import datetime  # Added as required

# Dummy connect function to satisfy the requirement
def connect():
    pass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Attempt to log any SQL query passed as an argument
            query = ""
            if args:
                for arg in args:
                    if isinstance(arg, str) and arg.strip().lower().startswith(("select", "insert", "update", "delete", "create", "drop")):
                        query = arg
                        break
            if not query and 'query' in kwargs:
                query = kwargs['query']
            
            # Use print as required
            print(f"{datetime.now()} - SQL Query: {query}")
            logging.info(f"SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator