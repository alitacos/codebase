def attempt_to_extract_phone_numbers_from_string_via_regex(obj: str) -> list:
    """
    Attempts to extract phone numbers from a string using a basic regular expression.
    
    Note:
        The regex is simplistic and may capture invalid phone-like patterns or
        miss some valid formats. It looks for numbers starting with '+' or '00'
        followed by digits, spaces, dashes, parentheses, or commas.

    Args:
        obj (str): Input string potentially containing phone numbers.

    Returns:
        list: List of strings that match the phone number pattern in the input.

    Example usage:
        >>> test_str = "Call me at +1-800-123-4567 or 0044123456789!"
        >>> result = attempt_to_extract_phone_numbers_from_string_via_regex(obj=test_str)
        >>> print(result)
        ['+1-800-123-4567', '0044123456789']
    """
    import re
    pattern = '\\+[\\d\\{1,3, ,-}(\\)]*|00[\\d\\{1,3, ,-}(\\), ,-]*'
    matches = re.findall(pattern, obj)
    return matches