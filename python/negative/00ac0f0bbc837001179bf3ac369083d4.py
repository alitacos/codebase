def get_non_ascii_chars_from_string(content:str='')->list:
    """
    >>> get_nonascii_chars(u'zur\\xc3\\xbcckf\\xc3\\xbchren.')
    [u'\\xc3\\xbc', u'\\xc3\\xbc']
    """
    chars = [u'']
    in_nonascii = False
    for char in content:
        if ord(char) > 127:
            chars[-1] += char
            in_nonascii = True
            continue
        if in_nonascii:
            in_nonascii = False
            chars.append(u'')
    if chars[-1] == u'':
        chars = chars[:-1]
    return chars