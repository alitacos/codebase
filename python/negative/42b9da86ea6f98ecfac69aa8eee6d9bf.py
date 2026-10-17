def remove_curly_brackerts_enclosed_text_from_string_via_regex(text: str='') -> str:
    """
        Removes text enclosed in curly braces `{}` from a string. Works with str, bytes, or bytearray inputs.

    Args:
        text (str): Input string (or bytes/bytearray) from which all `{...}` content will be removed. (Defaults to '')

    Returns:
        str: The input string with all curly-braced content removed, extra spaces normalized.

    Example usage:
        >>> result = remove_curly_brackerts_enclosed_text_from_string_via_regex(text='Hello {world}!')
        >>> print(result)
        Hello !
    """

    def bytes_to_str(text: str=None):
        try:
            text = text.decode(encoding='utf-8', errors='replace')  # Try UTF-8 decoding
        except Exception as e1:
            try:
                text = text.decode(encoding='latin-1', errors='replace')  # Fallback to Latin-1
            except Exception as e2:
                try:
                    text = text.decode(errors='ignore')  # Fallback to default decode, ignoring errors
                except Exception as e3:
                    text = ''  # Give up, return empty string
        return text

    if isinstance(text, (bytes, bytearray)):  # Convert bytes/bytearray to string
        text = bytes_to_str(text=text)

    if not text:  # Return empty string if input is None or empty
        return ''

    if not isinstance(text, str):  # Convert other types to string
        try:
            text = str(text)
        except Exception as e:
            text = ''

    import re  # Regex module for pattern matching
    item = re.sub('\\{.*?\\}', '', text)  # Remove text between { and } (non-greedy)

    # Normalize spaces: remove empty elements and strip extra spaces
    return ' '.join((i.strip(' ') for i in item.split(' ') if i.strip(' ')))

# Suggested improvements / notes:
# 1. Nested curly braces are not fully removed; only non-greedy matches are removed.
#    Example: "This [{'key':{'w':2}}] test" -> "This ['}] test"  # as in your warning
# 2. Consider using a parser or recursive regex for fully nested curly braces.
# 3. Current function works for bytes, bytearray, str, and most other types safely.
# 4. Extra spaces are normalized at the end using join + strip.
# 5. Regex pattern '\\{.*?\\}' could match unintended content if string contains '{' or '}' inside quotes.