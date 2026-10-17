def check_if_string_is_astParsable(code:str|bytes='')->bool:
    """
	    Check whether the provided source code can be successfully parsed
	    into a valid Python AST.

    Args:
        code (str | bytes): Python source code to validate with `ast.parse`.
        (Defaults to '')

    Returns:
        bool: True if the source code is AST-parseable; otherwise False.

    Example usage:
        >>> result = check_if_string_is_astParsable(code='print("hello")')
    	"""
    if not isinstance(code, (str,bytes)):
        return False
    try:
        ast.parse(code)
        return True
    except Exception:
        return False