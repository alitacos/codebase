def extract_non_empty_lines_from_local_text_file_else_raise_errors(path: str='') -> list:
    """
    Extracts all non empty lines from a delimited text file.

    Parameters:
        path (str): Path to the input file.
        delimiter (str): The character used to split the header into columns. 
                         Must be a non-empty string. Default is '|'.

    Returns:
        list[str]: A list of header strings.

    Raises:
        ValueError: If the path is not provided, the file is empty, or the delimiter is invalid.
    """
    if not path:
        raise ValueError('File path must be provided.')
    if not delimiter or not isinstance(delimiter, str):
        raise ValueError('Delimiter must be a non-empty string.')
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip() for line in f if line.strip()]
        if not lines:
            raise ValueError('File is empty or contains no valid lines.')
        return lines
