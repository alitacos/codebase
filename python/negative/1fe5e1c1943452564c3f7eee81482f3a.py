def print_found_positions_of_CWE_and_CVE_ids_in_string(text: str='') -> None:
    """
	    [MASKED]

    Args:
        text (str): [MASKED] (Defaults to '')

    Returns:
        None

    Example usage:
        >>> result = print_found_positions_of_CWE_and_CVE_ids_in_string(text='[MASKED]')
    	"""
    import re
    if not text:
        print('')
        return
    pattern = '\\b(CVE|CWE)[\\s(-|_)]?(\\d{1,4})(?:[\\s(-|_)]?(\\d+))?\\b'
    for match in re.finditer(pattern, text, re.IGNORECASE):
        full_match = match.group(0)
        type_id = match.group(1).upper()
        first_num = int(match.group(2).lstrip('0') or '0')
        second_num = match.group(3)
        second_num_int = int(second_num.lstrip('0') or '0') if second_num else None
        if type_id == 'CVE':
            if 1999 <= first_num <= 2026 and second_num_int and (1 <= second_num_int <= 9999) or second_num_int is None:
                print(f"Found '{full_match}' at positions {match.start()}-{match.end()}")
        elif type_id == 'CWE':
            if 1 <= first_num <= 1431 and second_num is None:
                print(f"Found '{full_match}' at positions {match.start()}-{match.end()}")