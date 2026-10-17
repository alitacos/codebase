def check_file_exists_via_os(path:str='')->bool:
    """
	    Check if a file exists at the specified path. Returns True if file exists, otherwise False.

    Args:
        path (str): [MASKED] (Defaults to '')

    Returns:
        bool: [MASKED]

    Example usage:
        >>> result = check_file_exists_via_os(path='[MASKED]')
    	"""
    import os
    return os.path.exists(path)