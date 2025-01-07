import json
import os
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


def write_as_json(result, path) -> ():
    file_path = path if path.startswith('/') else os.path.join(get_root_path(), path)
    with open(file_path, "w") as temp_file:
        json.dump(result, temp_file, indent=2)


def get_root_path() -> str:
    current_path = Path(__file__).resolve()
    root_path = current_path.parent
    while root_path.name != "tests":
        root_path = root_path.parent
    root_path = root_path.parent  # Get the parent of 'tests'
    return str(root_path)
