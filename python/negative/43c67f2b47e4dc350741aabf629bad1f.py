def load_binary_file_as_numpy(path:str='', columns_count:int=0):
    """
	    [MASKED]

    Args:
        path (str): [MASKED] (Defaults to '')
        columns_count (int): [MASKED] (Defaults to 0)

    Returns:
        Any: [MASKED]

    Example usage:
        >>> result = load_binary_file_as_numpy(path='[MASKED]', columns_count='[MASKED]')
    	"""
    import numpy as np
    try:
        return np.fromfile(path, dtype=np.uint8).reshape(-1, num_services)
    except Exception:
        return None