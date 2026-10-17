import ast
def extract_all_functions_by_iter_child_nodes_in_AstNode(node:ast.AST=None)->list:
    functions = []
    if not node:
        return functions
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


#extract_all_functions_by_iter_child_nodes_in_AstNode("""was ist a, \ndef foo(a,/,  b: int, c='hello', *,l):\n\tpass""")#[out]:[] 
#extract_all_functions_by_iter_child_nodes_in_AstNode("""#was ist a, \ndef foo(a,/,  b: int, c='hello', *,l):\n\tpass""")#[out]:  []
#extract_all_functions_by_iter_child_nodes_in_AstNode(ast.parse("""#was ist a, \ndef foo(a,/,  b: int, c='hello', *,l):\n\tpass"""))#[out]:  []
#extract_all_functions_by_iter_child_nodes_in_AstNode(ast.parse("""#was ist a, \ndef foo(a,/,  b: int, c='hello', *,l):\n\tpass""").body)#[out]:  []
#extract_all_functions_by_iter_child_nodes_in_AstNode(ast.parse("""def foo(a,/,  b: int, c='hello', *,l):\n\tpass""").body[0])#[out]:  []
