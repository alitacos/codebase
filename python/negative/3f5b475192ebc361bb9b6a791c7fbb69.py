# would not work without the expected imports
def remove_docstring_action(func_code_content: str) -> str:
    """
    Removes any existing docstring from the given function code.
    """
    if not func_code_content.strip():
        return ''
    modified_code = _remove_existing_docstring(func_code_content)
    return modified_code