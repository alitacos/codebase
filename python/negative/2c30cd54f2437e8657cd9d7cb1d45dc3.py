# works but is prefered using type hints, output hints, exception handling
import ast
def walk_functions(node:ast.Ast=None)->list:
    """
	    Recursively collects all functions and async functions from an AST node, including those inside classes.

    Args:
        node (ast.AST): The AST node to search for function definitions.

    Returns:
        list: A list of tuples where each tuple contains the AST node and its corresponding source code as a string.

    Example usage:
        >>> result = walk_functions(node=some_ast_tree)
    """
    import textwrap
    functions = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            code = textwrap.dedent(ast.unparse(child))
            functions.append((child, code))
            functions.extend(walk_functions(child))
        elif isinstance(child, ast.ClassDef):
            functions.extend(walk_functions(child))
    return functions