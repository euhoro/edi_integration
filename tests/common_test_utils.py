import json
import os
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path


def read_as_str(path:str) -> str:
    file_path = path if path.startswith('/') else os.path.join(get_root_path(), path)
    with open(file_path, "r") as file:
        file_data = file.read()  # Read the entire file as a string.
        return file_data


def read_as_json(path) -> dict:
    file_path = path if path.startswith('/') else os.path.join(get_root_path(), path)
    with open(file_path, "r") as file:
        file_data = json.load(file)  # Parse the JSON file into a dictionary
        return file_data


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, datetime):
        #     return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(f"{obj:.2f}")  # Convert to float with fixed 2 decimal places
        # Add support for Pydantic models
        if hasattr(obj, "model_dump"):  # Handle Pydantic models
            res = obj.model_dump()  # Dump the model first
            res = remove_nulls(res)  # Remove nulls recursively from the dumped model data
            return res
        return super().default(obj)

def write_as_json(result, file_path , cls = None) -> ():
    file_path = file_path if file_path.startswith('/') else os.path.join(get_root_path(), file_path)
    # with open(file_path, "w") as temp_file:
    #     json.dump(data, temp_file, indent=2)

    # Remove null values from the data
    # clean_data = remove_nulls(result)

    if cls is None:
        with open(file_path, 'w') as f:
            json.dump(result, f, cls=DateTimeEncoder, indent=2)
    else:
        with open(file_path, 'w') as f:
            json.dump(result, f, indent=2)

def remove_nulls(obj):
    """Recursively remove keys with None values from dictionaries."""
    if isinstance(obj, dict):
        return {k: remove_nulls(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_nulls(item) for item in obj]
    else:
        return obj

def get_root_path() -> str:
    current_path = Path(__file__).resolve()
    root_path = current_path.parent
    while root_path.name != "tests":
        root_path = root_path.parent
    root_path = root_path.parent  # Get the parent of 'tests'
    return str(root_path)
