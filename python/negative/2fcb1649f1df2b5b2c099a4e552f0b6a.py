import ast
def collect_all_FunctionDef_nodes_in_ast_node(node:ast.Module|ast.FunctionDef=None)->list:  # collects function definitions from AST or source
    """
    Recursively collects all FunctionDef and AsyncFunctionDef nodes from a Python AST or source code.

    This function extracts function definitions found in:
    - top-level module scope
    - nested structures (e.g., inside classes or other nodes)

    Args:
        node (ast.Module | ast.FunctionDef | str | bytes):
            An AST node, function node, or raw Python source code.

    Returns:
        list:
            A list of all FunctionDef and AsyncFunctionDef AST nodes found.

    Example usage:
        >>> result = collect_all_FunctionDef_nodes_in_ast_node(node='[Python source code]')
    """
    #excludes top level classes, methods inside clases etc
    functions = []
    if isinstance(node, (str, bytes)):
        try:
            node = ast.parse(node)
        except Exception as e:
            #print(e)
            return []   
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): #ywes
        functions.append(node)
        return functions
    try:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(child)
                for chd in collect_all_function_nodes_from_ast(child):
                    if chd not in functions:
                        functions.append(chd)
            elif isinstance(child, ast.ClassDef):
                functions.append(child)
                for chd in collect_all_function_nodes_from_ast(child):
                    if chd not in functions:
                        functions.append(chd)
        return functions
    except Exception as e1:
        #print(e1)
        return []