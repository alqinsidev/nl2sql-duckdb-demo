import requests
from typing import Any, Dict, Optional
from .logger import logger

def safe_request(
    method: str,
    url: str,
    timeout: int = 10,
    **kwargs
) -> Optional[Dict[str, Any]]:
    """
    Performs a safe HTTP request with error handling and logging.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        url: Target URL
        timeout: Request timeout in seconds (default: 10)
        **kwargs: Additional arguments passed to requests.request
        
    Returns:
        JSON response as a dictionary, or None if the request failed.
    """
    try:
        logger.info(f"Making {method} request to {url}")
        response = requests.request(method, url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e}")
        return {"error": f"HTTP Error: {e}", "status_code": response.status_code}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection Error: {e}")
        return {"error": f"Connection Error: {e}"}
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout Error: {e}")
        return {"error": f"Timeout Error: {e}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Exception: {e}")
        return {"error": f"Request Exception: {e}"}
    except ValueError as e:
        logger.error(f"JSON Decode Error: {e}")
        return {"error": "Invalid JSON response"}
