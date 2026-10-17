def generate_block_numbers_by_range(r: range = range(0, 0), prefix: str = '+49'):
    """
    Generates a list of prefixed numeric strings based on a given numeric range.

    The function takes a range of integers and attaches a prefix (e.g. country code, area code, or any identifier)
    to each number in the range, producing a sequence of formatted "block numbers".

    Args:
        r (range): Range of integers used as the numeric block source. (Defaults to empty range range(0, 0))
        prefix (str): String prefix to prepend to each number (e.g. '+49', 'BLOCK-', 'ID-'). (Defaults to '+49')

    Returns:
        list: A list of strings where each element is prefix + number from the range.
              Returns an empty list if the range is empty or invalid.

    Example usage:
        >>> result = generate_block_numbers_by_range(r=range(1000, 1005), prefix='+49')
        >>> print(result)
        ['+491000', '+491001', '+491002', '+491003', '+491004']
    """
    if not r or r == range(0, 0):  # guard clause for empty/default range
        return []  # return empty list if no valid range provided

    return [f'{prefix}{i}' for i in r if i]  # generate prefixed values for each number in range