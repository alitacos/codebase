# NEGATIVE

import ast
def unparse_arguments(arguments: ast.arguments) -> str:
    """
    Unparses ast.arguments into a string and returns both the string 
    and a dictionary mapping parts to their respective AST nodes.
    """
    parts = []
    args_dict = {}

    # 1. Positional-only args
    for arg in arguments.posonlyargs:
        text = ast.unparse(arg)
        parts.append(text)
        args_dict[text] = arg
    
    if arguments.posonlyargs:
        parts.append("/")
        args_dict["/"] = "/"

    # 2. Regular args (positional or keyword)
    defaults = arguments.defaults
    n_defaults = len(defaults)
    n_regular = len(arguments.args)
    first_default = n_regular - n_defaults

    for i, arg in enumerate(arguments.args):
        text = ast.unparse(arg)
        if i >= first_default:
            default_val = ast.unparse(defaults[i - first_default])
            full_text = f"{text}={default_val}"
            parts.append(full_text)
            args_dict[full_text] = arg
        else:
            parts.append(text)
            args_dict[text] = arg

    # 3. Varargs (*args) or bare *
    if arguments.vararg:
        text = "*" + ast.unparse(arguments.vararg)
        parts.append(text)
        args_dict[text] = arguments.vararg
    elif arguments.kwonlyargs:
        parts.append("*")
        args_dict["*"] = "*"

    # 4. Keyword-only args
    for arg, default in zip(arguments.kwonlyargs, arguments.kw_defaults):
        text = ast.unparse(arg)
        if default is not None:
            default_val = ast.unparse(default)
            full_text = f"{text}={default_val}"
            parts.append(full_text)
            args_dict[full_text] = arg
        else:
            parts.append(text)
            args_dict[text] = arg

    # 5. Kwargs (**kwargs)
    if arguments.kwarg:
        text = "**" + ast.unparse(arguments.kwarg)
        parts.append(text)
        args_dict[text] = arguments.kwarg

    full_string = ", ".join(parts)
    print("--- Arguments Mapping ---")
    for k, v in args_dict.items():
        print(f"{k}: {v}")
    
    return full_string
 