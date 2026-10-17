def extract_code_string_from_outcommented_text(text:str=None)->str:
    #assuming the text was previously a text and we mark with '#' any lines that are not code before we pass it in this function. 
    import ast
    code = None
    try:
        node = ast.parse(text)
        code =  ast.unparse(node)
    except Exception as e:
        try:

            node = ast.parse(text)
            code =  ast.unparse(node)
        except Exception as e1:
            code =  None
    return code