def check_if_bytes_or_string_is_astParsable_with_extension_filters(code: str | bytes = '', allowStr: bool = False, allowBodyList:bool=False) -> bool:
    """
        Check whether the input (bytes/str/bytearray) can be parsed into valid Python
        AST using ast.parse(), with optional extended behaviors for:
        - allowing string inputs (allowStr)
        - evaluating list-like structures before parsing (allowBodyList)

    Args:
        code (str | bytes): Input Python source code or byte representation.
            Default is empty string. Must be compatible with AST parsing rules.
        allowStr (bool): If True, allows plain string inputs to be parsed.
            If False, string inputs may be rejected depending on logic path.
        allowBodyList (bool): If True, allows evaluation of the input into a Python
            object and treats list outputs as AST-unparseable intermediate structures.

    Returns:
        bool: True if the input can be successfully processed into valid AST
        via ast.parse() under the selected flags; otherwise False.
        
        
        """
    import ast
    if allowBodyList and isinstance(code, (str,bytes,bytearray)):
        try:
            body = eval(code)
            if isinstance(body, list):
                code = ast.unparse(code)
                ast.parse(code)
                if not allowStr and isinstance(code, str):
                    return False
                return True
        except Exception as e:
            return False  
    if not allowStr and isinstance(code,str):
        return False  
    if isinstance(code, (bytes,bytearray)) or (allowStr and isinstance(code, str)):
        try:
            code = ast.parse(code)
            return True
        except Exception as e:
            return False
        return False # ensure False
    return False # ensure False