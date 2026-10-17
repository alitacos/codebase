#works but is prefered exception handling
def remove_quoted_sub_string_via_regex(text: str='', quote: str='"', seq: int=3) -> str:
    ''''
	    Removes substrings enclosed within repeated quote characters using a regex pattern, then returns the cleaned text with extra whitespace removed.

    Args:
        text (str): The input text from which quoted substrings will be removed (Defaults to '')
        quote (str): The quote character used to identify substrings (Defaults to '"')
        seq (int): Number of repeated quote characters to identify the substring boundaries (Defaults to 3)

    Returns:
        str: Text with the specified quoted substrings removed and extra spaces stripped

    Example usage:
        >>> result = remove_quoted_sub_string_via_regex(text='Here is """a quoted""" text', quote='"', seq=3)
    '''
    #try:
    pattern = f'\\{quote}{{{seq}}}(.*?)\\{quote}{{{seq}}}'
    item = re.sub(pattern, '', text)
    return ' '.join((i.strip() for i in item.split() if i.strip()))
    #except Exception as e:
        #return ''