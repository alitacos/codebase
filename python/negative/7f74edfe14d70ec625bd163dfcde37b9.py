def generate_block_numbers_by_range(r: range=range(0, 0), prefix: str='+49'):
    """
	    [MASKED]

    Args:
        r (range): [MASKED] (Defaults to range(0, 0))
        prefix (str): [MASKED] (Defaults to '+49')

    Returns:
        Any: [MASKED]

    Example usage:
        >>> result = generate_block_numbers_by_range(r='[MASKED]', prefix='[MASKED]')
    	"""
    if not r or r == range(0, 0):
        return []
    return [f'{prefix}{i}' for i in r if i]