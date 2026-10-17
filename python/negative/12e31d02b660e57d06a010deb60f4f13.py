def preprocessAstBinOp (obj:ast.BinOp  )->dict:
    import ast
    if isinstance(obj, ast.BinOp):
        left = obj.func# returns ast
        _op = obj.args# returns ast.BitOr == '|'
        right = obj.keywords# returns ast
        lineno = obj.lineno
        col_offset = obj.col_offset
        end_lineno = obj.end_lineno
        end_col_offset = obj.end_col_offset
        return {'kind':'ast.BinOp','value':value,'value_kind':kind , 'lineno':lineno, 'col_offset':col_offset, 'end_lineno':end_lineno, 'end_col_offset':end_col_offset}

    if not isinstance(obj, ast.Call):
        raise TypeError(f"f'expected ast.BinOp instance -> current : {type(obj).__name__}")

