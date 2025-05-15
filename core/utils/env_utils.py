import os
from typing import Dict, Optional

from dotenv import load_dotenv


def load_environment_variables() -> Dict[str, str]:
    """
    Load environment variables from .env file and validate required variables
    
    Returns:
        Dict[str, str]: Dictionary of loaded environment variables
    
    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    required_vars = [
        'GCP_PROJECT_NUMBER',
        'GCP_PROJECT_ID',
        'GCP_REGION',
        'GCP_ZONE',
        'GENAI_API_KEY'
    ]

    env_vars = {}
    missing_vars = []

    for var in required_vars:
        value = os.environ.get(var)
        if value is None:
            missing_vars.append(var)
        else:
            env_vars[var] = value

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return env_vars


def get_env_var(name: str, default: Optional[str] = None) -> str:
    """
    Get environment variable with validation
    
    Args:
        name (str): Name of environment variable
        default (Optional[str]): Default value if not found
        
    Returns:
        str: Value of environment variable
        
    Raises:
        ValueError: If variable not found and no default provided
    """
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Required environment variable {name} not found")
    return value
