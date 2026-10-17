def get_ast_tree_via_ast_for_py_string(code):
    try:
        import ast
        ast_code = ast.parse(code, mode='exec')
        return set([str(i) for i in ast_code.body])
    except Exception as e:
        return 'ERROR: ' + str(e)