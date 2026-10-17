import ast
def get_signature_of_FunctionDef_node(func_node: ast.FunctionDef|ast.AsyncFunctionDef=None) -> str:   
    """
    Extracts the signature of a Python function from an AST FunctionDef or AsyncFunctionDef node.
    
    Args:
        func_node (ast.FunctionDef | ast.AsyncFunctionDef): An AST node representing a function definition.
    
    Returns:
        str: A string representation of the function signature, including name, arguments, optional return type,
             and "async" prefix if applicable.
    
    Example usage:
        >>> result = get_signature_of_FunctionDef_node(func_node='[Python source code or AST node]')
    """
    def get_FunctionDef_node_of_ast(astTree:ast.Module=None, function_name:str=None)->ast.FunctionDef|ast.AsyncFunctionDef:
        try:
            for node in astTree.body:
                if isinstance(node, (ast.FunctionDef,ast.AsyncFunctionDef)) and node.name == function_name:
                    return node
            return None
        except Exception as e:
            return None  
    def get_signature1(func_node: ast.FunctionDef|ast.AsyncFunctionDef=None):
        try:
            args = ast.unparse(func_node.args)
            returns = ""
            if func_node.returns:
                returns = f" -> {ast.unparse(func_node.returns)}"
            return f"{func_node.name}({args}){returns}"        
        except Exception as e:
            return ''
    def get_signature2(func_node: ast.FunctionDef|ast.AsyncFunctionDef=None)->str:
        try:
            args = ast.unparse(func_node.args)
            returns = ''
            if func_node.returns: 
                returns = ( f' -> ' f'{ast.unparse(func_node.returns)}' )
            prefix = ''
            if isinstance( func_node, ast.AsyncFunctionDef ):
                prefix = 'async '
            return ( f'{prefix}{func_node.name}({args}){returns}' )
        except Exception:
            return ''

            
    if not func_node:
        return ''
    if not isinstance(func_node, (ast.FunctionDef,ast.AsyncFunctionDef)):
        func_node =  get_FunctionDef_node_of_ast(astTree=func_node)
        if not isinstance(func_node, (ast.AsyncFunctionDef,ast.FunctionDef)):
            return ''                                                 
    return get_signature1(func_node) or get_signature2(func_node)
