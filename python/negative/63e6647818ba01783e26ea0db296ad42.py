def check_for_potential_python_SyntaxError_in_string_line_via_ast(line:str='')->bool:
    """
    Checks if a given string is invalid Python code by attempting to compile it and checking if has SyntaxError.

    Args:
        line (str): The string containing Python code to check.

    Returns:
        bool: True if the code is syntactically valid, False otherwise.
    """
    if not line or not isinstance(line,(str,bytes)) or not line.strip():
        return False
    try:
        compile(line_of_code, '<string>', 'exec')
        return True
    except SyntaxError:
        return False