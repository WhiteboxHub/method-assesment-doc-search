import os

# def get_all_file_paths(folder_path : str):

#     if not os.path.isdir(folder_path):
#         raise ValueError(f"The path '{folder_path}' is not a valid directory.")

#     pptx_files = [
#         os.path.join(folder_path, file)
#         for file in os.listdir(folder_path)
#         if file.lower().endswith('.pptx') and os.path.isfile(os.path.join(folder_path, file))
#     ]

#     return pptx_files

from pathlib import Path

def get_all_file_paths(folder_path: str):
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"The path '{folder_path}' is not a valid directory.")

    return [str(file.as_posix()) for file in folder.glob("*.pptx") if file.is_file()]
