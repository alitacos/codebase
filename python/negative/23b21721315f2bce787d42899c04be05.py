# would not work without the expected imports  <extract_function_info>
import ast
def extract_parsable_funcs(ast_tree:ast.AST =None)->list:
    """
	    Extract functions/methods from AST, recursively. 
        For each function: Remove unused imports,Remove duplicate imports, Prepend only missing required top-level imports,Validate function

    Args:
        ast_tree (Any): The AST tree of a Python module or script.

    Returns:
        list: A list of dictionaries containing 'code' (function source with necessary imports) and 'info' (function metadata).

    Example usage:
        >>> result = extract_parsable_funcs(ast_tree=ast.parse(''))
    	"""
    import textwrap
    top_imports = []
    for node in ast_tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_name = alias.asname or alias.name.split('.')[0]
                line = f'import {alias.name}' + (f' as {alias.asname}' if alias.asname else '')
                top_imports.append((line, imported_name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imported_name = alias.asname or alias.name
                line = f'from {module} import {alias.name}' + (f' as {alias.asname}' if alias.asname else '')
                top_imports.append((line, imported_name))
    top_imports = list(dict(top_imports).items())

    def walk_functions(node):
        functions = []
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                code = textwrap.dedent(ast.unparse(child))
                functions.append((child, code))
                functions.extend(walk_functions(child))
            elif isinstance(child, ast.ClassDef):
                functions.extend(walk_functions(child))
        return functions
    func_tuples = walk_functions(ast_tree)
    func_strings_with_imports = []
    for node, func_code in func_tuples:
        names_used = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
        local_imports = {}
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Import):
                for alias in subnode.names:
                    imp_name = alias.asname or alias.name.split('.')[0]
                    line = f'import {alias.name}' + (f' as {alias.asname}' if alias.asname else '')
                    local_imports[imp_name] = line
            elif isinstance(subnode, ast.ImportFrom):
                module = subnode.module or ''
                for alias in subnode.names:
                    imp_name = alias.asname or alias.name
                    line = f'from {module} import {alias.name}' + (f' as {alias.asname}' if alias.asname else '')
                    local_imports[imp_name] = line
        missing_imports = []
        for line, imp_name in top_imports:
            if imp_name in names_used and imp_name not in local_imports:
                missing_imports.append(line)
        final_code = '\n'.join(missing_imports) + ('\n\n' if missing_imports else '') + func_code
        try:
            ast.parse(final_code)
            func_info = extract_function_info(final_code)
            func_strings_with_imports.append({'code': final_code, 'info': func_info})
        except Exception:
            continue
    return func_strings_with_imports