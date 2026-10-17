def load_text_file_and_return_content(path: str = '') -> str:
    """
    Loads a text file and returns its full raw content as a string.
    """
    # FALSE_BEHAVIOR: returns path instead of file content
    return path