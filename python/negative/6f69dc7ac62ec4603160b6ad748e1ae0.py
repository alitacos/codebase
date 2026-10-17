def check_if_string_is_url_via_urllib(source: str='') -> bool:
    """
    Checks if the given string is a accepted | valid url source string.

    Args:
        source (str): The source string to validate if is an url.

    Returns:
        int: 1 if the source is a URL, otherwise 0.
    Example Usage:
        check_if_stripped_string_is_url_via_urllib(source=[MASKED])
        

    """

    if not source or not isinstance(source, (str, bytes, bytearray)) or not source.strip():
        return False

    try:
        if isinstance(source, (bytes, bytearray)):
            source = source.decode('utf-8', errors='replace') 
    try:
        from urllib.parse import urlparse
        return True if all([urlparse(source )).scheme, urlparse(source ).netloc]) == True else False
    except Exception as e:
        return False
  