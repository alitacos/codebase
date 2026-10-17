import ast
def simple_check_if_functionDef_node_has_explicit_return_statement(fnode:ast.FunctionDef|ast.AsyncFunctionDef|ast.Module=None)->bool:
    try:
        return any(isinstance(node, ast.Return) for node in ast.walk(fnode))
    except Exception as e:
        return False
