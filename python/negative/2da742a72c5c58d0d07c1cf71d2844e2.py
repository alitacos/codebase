def clean_docstring_from_single_function_string(func_code: str='') -> str:
    """
	    Removes the docstring from a Python function's code string, returning the function code without its docstring.

    Args:
        func_code (str): Python function code as a string. (Defaults to '')

    Returns:
        str: The function code with the docstring removed, or the original code if no docstring is found.

    Example usage:
        >>> result = clean_docstring_from_single_function_string(func_code='def foo():\n    """Example docstring"""\n    pass')
     """
    import ast
    try:
        if not func_code:
            return ''
        try:
            tree = ast.parse(func_code)
        except Exception:
            return func_code
        func_node = next((node for node in tree.body if isinstance(node, ast.FunctionDef)), None)
        if not func_node or not func_node.body:
            return func_code.strip()
        first_stmt = func_node.body[0]
        if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Constant) and isinstance(first_stmt.value.value, str):
            lines = func_code.splitlines(keepends=True)
            start = first_stmt.lineno - 1
            end = first_stmt.end_lineno
            new_lines = lines[:start] + lines[end:]
            return ''.join(new_lines).rstrip() + ''
        return func_code.strip()
    except Exception as e:
        print(e)
        return ''