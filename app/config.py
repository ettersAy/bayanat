import json
import os

CONFIG_FILE = "pg_client_config.json"

def load_config():
    """Loads the connection string from config file."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("connection_string", "")
        except Exception as e:
            print(f"Failed to load config: {e}")
    return ""

def save_config(conn_str):
    """Saves the connection string to config file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"connection_string": conn_str}, f)
    except Exception as e:
        print(f"Failed to save config: {e}")
