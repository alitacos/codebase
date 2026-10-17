import ast

def clean_body_from_top_level_imports_and_constants(node:ast.AST=None)->list:
    """
    Removes non-functional top-level AST nodes such as imports and standalone constants (including module-level docstrings), returning a filtered list of remaining AST statements. This is a structural cleanup utility that operates only on the top-level module body and does not modify nested structures or evaluate code semantics.

    Args:
        node (ast.AST): A parsed AST module node expected to contain a `.body` attribute representing top-level statements. If None or invalid, the function returns an empty list.

    Returns:
        list: A list of AST nodes representing the cleaned top-level body, excluding Import, ImportFrom, and standalone constant expression nodes. Returns an empty list if input is invalid or an error occurs during processing.

    Example usage:
        >>> result = clean_body_from_top_level_imports_and_constants(node=ast.parse("import os\\ndef f(): pass"))
    """
    clean_body = []  # list to store filtered AST nodes
    if not node:  # handle None or falsy input safely
        return clean_body

    try:
        for item in node.body:  # iterate over top-level AST nodes in module body
            if isinstance(item, (ast.Import, ast.ImportFrom)):  # remove import statements
                continue
            if isinstance(item, ast.Expr) and isinstance(getattr(item, "value", None), ast.Constant):  # remove standalone constants / docstrings
                continue
            clean_body.append(item)  # keep all other executable or structural nodes
    except Exception as e:  # catch unexpected AST structure errors
        return []  # fail-safe return for malformed input