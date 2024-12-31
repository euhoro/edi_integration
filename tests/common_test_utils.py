from pathlib import Path


def get_root_path() -> str:
    current_path = Path(__file__).resolve()
    root_path = current_path.parent
    while root_path.name != "tests":
        root_path = root_path.parent
    root_path = root_path.parent  # Get the parent of 'tests'
    return str(root_path)