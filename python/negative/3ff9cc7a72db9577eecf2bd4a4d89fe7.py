import ast
def count_all_FunctionDef_nodes_in_ast_node(node:ast.Module|ast.FunctionDef=None)->int:
    """
    Recursively counts all FunctionDef and AsyncFunctionDef nodes within a given AST node or source string.

    Args:
        node (ast.Module | ast.FunctionDef | str | bytes): The AST node or source code to analyze.

    Returns:
        int: The total count of function definitions found within the node.

    Example usage:
        >>> result = count_all_FunctionDef_nodes_in_ast_node(node='def a():\n  def b(): pass')
    """
    functions = []
    # Convert string or bytes input into an AST node
    if isinstance(node, (str, bytes)):
        try:
            node = ast.parse(node)
        except Exception as e:
            #print(e)
            return 0
    # If the provided node is already a function definition, count it and return
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        functions.append(node)
        return len(functions)
    try:
        # Iterate through child nodes to find and collect function definitions
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(child)
                # Recurse into the function body to find nested functions
                functions.extend(collect_all_function_nodes(child))
            elif isinstance(child, ast.ClassDef):
                # Recurse into class definitions to find methods
                functions.extend(collect_all_function_nodes(child))
        return len(functions)
    except Exception as e1:
        #print(e1)
        return 0