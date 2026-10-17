import ast

def get_docstring_of_FunctionDef_node_in_src_ast_node_by_idx_without_error_raise(
    func_node: ast.AST|ast.FunctionDef|ast.AsyncFunctionDef|str|bytes =None,
    idx: int|str = 0
) -> str:    
 
    def get_top_level_functions(astTree):
        try:
            return [
                n for n in astTree.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
        except Exception:
            return []

    def get_docstring(function_node):
        try:
            doc = ast.get_docstring(function_node)
            return doc.strip() if doc else ''
        except Exception:
            return ''

    if not func_node:
        return ''

    # handle bytes
    if isinstance(func_node, (bytes, bytearray)):
        func_node = func_node.decode('utf-8')

    # handle source code
    if isinstance(func_node, str):
        func_node = ast.parse(func_node)

    # must be AST now
    if isinstance(func_node, ast.AST) and not isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        funcs = get_top_level_functions(func_node)

        if not funcs:
            return ''

        # normalize idx
        if idx == "first":
            idx = 0
        elif idx == "last":
            idx = -1

        try:
            func_node = funcs[idx]
        except Exception:
            return ''

    if isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return get_docstring(func_node)

    return ''