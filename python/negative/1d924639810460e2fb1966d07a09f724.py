def clean_body_from_top_level_imports_and_constants(node:ast.AST=None)->ast.AST|None:
    """
    Removes non-functional top-level AST nodes such as imports and standalone constants (including module-level docstrings), returning a filtered list of remaining AST statements. This is a structural cleanup utility that operates only on the top-level module body and does not modify nested structures or evaluate code semantics.

    Args:
        node (ast.AST): A parsed AST module node expected to contain a `.body` attribute representing top-level statements. If None or invalid, the function returns an empty list.

    Returns:
        list: A list of AST nodes representing the cleaned top-level body, excluding Import, ImportFrom, and standalone constant expression nodes. Returns an empty list if input is invalid or an error occurs during processing.

    Example usage:
        >>> result = clean_body_from_top_level_imports_and_constants(node=ast.parse("import os\\ndef f(): pass"))
    """
    def functreebodylist2func(body_list: list[ast.stmt]) -> ast.AST:
        try:
            return ast.Module(body=body_list, type_ignores=[])
        except Exception:
            return  None

    if not node:
        return None
    try:
        if not isinstance(node, (str,bytes)):
            try:
                node = ast.parse(node)
                node_body = node.body
            except Exception as e:
                return None
        if isinstance(node, ast.AST) and not hasattr(node, "body") or (isinstance(node, ast.AST) and not isinstance(node.body, list)):
            return None
        if not isinstance(node, ast.AST):
            #node = ast.parse(node)
            node_body = node.body
        if isinstance(node, list):
            for i in node:
                if not isinstance(i, ast.AST):
                  return None
            node_body = node
            node = functreebodylist2func(node_body)
        #if len(node.body) == 1 isinstance(node, (ast.AsyncFunctionDef,ast.FunctionType, ast.AsyncFunctionDef))   :
        #    return node.body[0]
        for item in node.body:  # iterate top-level AST nodes
            if isinstance(item, (ast.Import, ast.ImportFrom,ast.Assign)):
                node.body.remove(item)
            else:
                return node
                #break
        return node
    except Exception as e:
        return None



