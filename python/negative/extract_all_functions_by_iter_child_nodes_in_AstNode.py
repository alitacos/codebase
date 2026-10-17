import ast
def extract_all_functions_by_iter_child_nodes_in_AstNode(node:ast.FunctionDef, ast.AsyncFunctionDef=None)->list:
    functions = []
    try:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(child)
                functions.extend(walk_functions(child))
            elif isinstance(child, ast.ClassDef):
                functions.extend(walk_functions(child))
        return functions
    except Exception as e:
        #print(e)
        return []