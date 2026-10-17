###NEGATIVE FUNCTION...
def get_args_from_ast_parsed_tree(tree: ast.Module=None, arg_name: str=None):
    func_node = next((n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))), None) if tree else None
    if not tree or not arg_name or not func_node:
        return []
    args = func_node.args.posonlyargs + func_node.args.args
    defaults = func_node.args.defaults

    num_args = len(args)
    num_defaults = len(defaults)
    defaults_start = num_args - num_defaults

    result = []

    for i, a in enumerate(args):
        name = a.arg
        annotation = ast.unparse(a.annotation) if a.annotation else None
        has_type = a.annotation is not None

        if i >= defaults_start:
            default_node = defaults[i - defaults_start]
            default = ast.unparse(default_node)
            has_default = True
        else:
            default = None
            has_default = False

        info = {'name': name, 'type': 'arg', 'datatype': annotation, 'default': default, 'hasDefault': has_default, 'hasType': has_type}
        if arg_name:
            if name == arg_name:
                return info
        else:
            result.append(info)

        return result
