import ast
def get_first_FunctionDef_node_in_ast_node(astTree:ast.Module=None, function_name:str=None)->ast.FunctionDef|ast.AsyncFunctionDef:
    """
    Retrieves the first top-level FunctionDef or AsyncFunctionDef node from a Python AST or source code.
    
    The function can optionally filter by function name. It supports multiple input types including:
    - raw Python source code (str)
    - parsed AST Module
    - direct FunctionDef / AsyncFunctionDef nodes
    
    Args:
        astTree (ast.Module | str | ast.FunctionDef | ast.AsyncFunctionDef):
            A Python AST module, function node, or raw source code string to analyze.
    
        function_name (str):
            Optional name filter used to return only a function matching this name.
    
    Returns:
        ast.FunctionDef | ast.AsyncFunctionDef | None:
            The first matching function node if found, otherwise None.
    
    Example usage:
        >>> result = get_first_FunctionDef_node_in_ast_node(astTree='[source code]', function_name='my_func')
    """
    try:
        for node in astTree.body:
            if isinstance(node, (ast.FunctionDef,ast.AsyncFunctionDef)) and node.name == function_name:
                return node
        return None
    except Exception as e:
        return None