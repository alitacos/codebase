def name??(code: str, output: object):
    try:
        result = eval(code, {})
    except SyntaxError:
        local_vars = {}
        exec(code, {}, local_vars)
        result = local_vars.get('result', None)
    return result == output