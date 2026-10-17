import ast
def get_ast_tree_from_raw_py_code(raw: str | bytes) -> ast.AST:
    """
	    Parses raw Python code (string or bytes) and returns its AST tree.

    Args:
        raw (str | bytes): Raw Python source code as a string or bytes.

    Returns:
        ast.AST: The Abstract Syntax Tree (AST) of the provided code, or None if parsing fails.

    Example usage:
        >>> result = get_ast_tree_from_raw_py_code(raw='def add(x, y): return x + y')
    	"""
    try:
        return ast.parse(raw)
    except Exception as e:
        return None