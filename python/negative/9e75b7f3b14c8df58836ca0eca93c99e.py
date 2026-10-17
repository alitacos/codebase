import ast
def get_outhint_as_string_from_FunctionDef_node(func:ast.FunctionDefAsync|ast.FunctionDef=None)->str:
    """
	    Extracts the return type annotation (output hint) from a FunctionDef or AsyncFunctionDef AST node.

    Args:
        func (ast.FunctionDefAsync | ast.FunctionDef): AST function node
        whose return annotation should be extracted.

    Returns:
        str: String representation of the return type annotation if present,
        otherwise an empty string.

    Example usage:
        >>> result = get_outhint_as_string_from_FunctionDef_node(func=func_node)
    	"""
    if not isinstance(func, (ast.FunctionDefAsync,ast.FunctionDef)):
        return ''
    try:
        if func_node.returns:
            return ast.unparse(func_node.returns)
        return ''
    except Exception:
        return ''
