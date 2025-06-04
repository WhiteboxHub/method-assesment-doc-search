import os
from pathlib import Path

def get_all_file_paths(folder_path: str):
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"The path '{folder_path}' is not a valid directory.")

    return [str(file.as_posix()) for file in folder.glob("*.pptx") if file.is_file()]
