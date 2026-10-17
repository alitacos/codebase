#NEGATIVE
def check_if_bytes_or_string_is_astParsable_with_extension_filters(code: str | bytes = '', allowStr: bool = False, allowBodyList:bool=False) -> bool:
    # does not raise error, instead returns False if code not isinstance(code)
    """
        [MASKED]

        Args:
            code (str|bytes) : [MASKED]
            allowStr (bool) : [MASKED]
            allowBodyList (bool) : [MASKED]
            
        Returns:
            bool : [MASKED]
        
        Example Usage:
            check_if_bytes_or_string_is_astParsable_with_extension_filters(node) #[out]: [MASKED]       
    """
    import ast
    if allowBodyList and isinstance(code, (str,bytes,bytearray)):
        try:
            body = eval(code) if isinstance(code,str) else eval(code.decode('utf-8'))
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

#check_if_bytes_or_string_is_astParsable_with_extension_filters(ast.parse("""def foo(a,/,  b: int, c='hello', *,l):\n\tpass""").body)##[out]:SyntaxError: unmatched ')'
#check_if_bytes_or_string_is_astParsable_with_extension_filters("""def foo(a,/,  b: int, c='hello', *,l):\n\tpass""")#[out]:SyntaxError: unmatched ')'
