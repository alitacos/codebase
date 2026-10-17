#add a better universal descriptive name. 
# missing exception handling. missing preprocessing
def verify_python_code_exec_returns_exact_output(code: object=None, output: object=None):
    """
	    Executes Python code exactly as provided and checks if its execution result matches the expected output without any post-processing.

    Args:
        code (object): The Python code to execute exactly as given
        output (object): The expected output to compare against

    Returns:
        Any: True if the executed code matches the expected output exactly, False otherwise

    Example usage:
        >>> result = verify_python_code_exec_returns_exact_output(code='x = 2 + 2', output=None)
    	"""
    # meaning we do not process the code output to clean from 
    if exec(code) == output:
        return True
    else:
        return False