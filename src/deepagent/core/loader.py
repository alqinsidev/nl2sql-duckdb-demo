import importlib
import pkgutil
import os
from typing import List, Any
from .logger import logger

def load_tools(package_name: str = "deepagent.tools") -> List[Any]:
    """
    Dynamically load tools from the specified package.
    Expects modules in the package to have a 'tool' attribute or a 'tools' list.
    """
    tools = []
    
    # Import the package to get its path
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        logger.error(f"Could not import package {package_name}: {e}")
        return []

    if not hasattr(package, "__path__"):
        logger.error(f"Package {package_name} has no path")
        return []

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
            
            # Check for single tool
            if hasattr(module, "tool"):
                tools.append(module.tool)
                logger.info(f"Loaded tool from {module_name}")
            
            # Check for list of tools
            elif hasattr(module, "tools") and isinstance(module.tools, list):
                tools.extend(module.tools)
                logger.info(f"Loaded tools from {module_name}")
                
        except Exception as e:
            logger.error(f"Failed to load module {module_name}: {e}")
            
    return tools
