import ast
def get_top_level_imports_in_ast_node(ast_tree:as.Ast=None)->list:
    imports = []
    try:
        for node in ast_tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f'{module}.{alias.name}')
    except Exception:
        pass
    return sorted(set(imports))
