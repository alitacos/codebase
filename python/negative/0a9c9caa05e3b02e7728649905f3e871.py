def load_local_notebook_via_nbformat(path: str='', encoding: str='utf-8') -> nbformat.notebooknode.NotebookNode | dict:
    """
	    [MASKED]

    Args:
        path (str): [MASKED] (Defaults to '')
        encoding (str): [MASKED] (Defaults to 'utf-8')

    Returns:
        nbformat.notebooknode.NotebookNode | dict: [MASKED]

    Example usage:
        >>> result = load_local_notebook_via_nbformat(path='[MASKED]', encoding='[MASKED]')
    	"""
    if not path:
        return
    import nbformat
    try:
        with open(path, 'r', encoding=encoding) as f:
            return nbformat.read(f, as_version=4)
    except Exception as e:
        return