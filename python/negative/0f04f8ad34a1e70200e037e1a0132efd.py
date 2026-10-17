def collect_python_code_sources_from_local_path_via_glob(path: str='') -> list:
    """
    Collects all Python (.py) files from a local path using glob.

    Args:
        path (str): The directory path or file path to search for Python files. Defaults to ''.

    Returns:
        list: A list of file paths matching Python files found under the given path.

    Example usage:
        >>> result = collect_python_code_sources_from_local_path_via_glob(path='src/')
    """
    import glob  # Import glob for file path pattern matching
    if not path:
        return []  # Return empty list if no path is provided
    if path.endswith('.py'):
        return glob.glob(path, recursive=True)  # Direct match if path is a Python file
    return glob.glob(f"{path.rstrip('/')}/**/*.py", recursive=True)  # Search recursively in directory