# File: utils.py
# Desc: Utility functions used my multiple files
import tomllib
import os 

def load_config(config_path="/app/config.toml"):
    """Load all params from config file with better error handling"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    
    try:
        with open(config_path, 'rb') as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"TOML parsing error in {config_path}: {str(e)}") from e
    except Exception as e:
        # Catch any other file reading errors
        raise RuntimeError(f"Failed to read config file {config_path}: {str(e)}") from e
