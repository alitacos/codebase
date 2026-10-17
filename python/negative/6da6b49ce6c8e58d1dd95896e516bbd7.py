#missing exception handling
def write_output(filename: str='', data: list=[], mode='a+')->None:
    """
	    Write a list of strings to a file using the specified file mode.

    Args:
        filename (str): Path to the file where the data should be written (Defaults to '')
        data (list): List of string entries that will be written line by line to the file (Defaults to [])
        mode (Any): File open mode used when writing the data to the file (Defaults to 'a+')

    Returns:
        None

    Example usage:
        >>> result = write_output(filename='output.txt', data=['value1','value2'], mode='a+')
    	"""
    with open(filename, mode=mode if mode else 'r') as f:
        for i in data:
            f.write(i + '\n')
        print('data successfully stored in ' + filename)
        return None