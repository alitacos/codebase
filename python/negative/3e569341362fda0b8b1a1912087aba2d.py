# non reusable class method... missing exception handling. Works only if input is carefully selected.
from typing import Any, Optional
import os

def ensure_file_and_directory_paths_exist(self: Any) -> None:
    """
	    Ensures that all file and directory paths stored as string attributes in the object's __dict__ exist.
        If a file path does not exist, it creates the necessary directories and an empty file.
        If a directory path does not exist, it creates the directory.

    Args:
        self (Any): The object whose string attributes represent file or directory paths.

    Returns:
        None: This function does not return any value.

    Example usage:
        >>> result = ensure_file_and_directory_paths_exist(self='[MASKED]')
    	"""
    for k, p in self.__dict__.items():
        if not isinstance(p, str):
            continue
        if os.path.splitext(p)[1]:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            if not os.path.exists(p):
                with open(p, 'w', encoding='utf-8'):
                    pass
        else:
            os.makedirs(p, exist_ok=True)
    return None
