def extract_nested_json_keys_via_json_load_into_tuple_from_string(s: str='') -> tuple:
    """
	    Retrieve first layer and nested keys from a json string

    Args:
        file_path (str): [MASKED] (Defaults to '')

    Returns:
        tuple: [MASKED]

    Example usage:
        >>> result = extract_nested_json_keys_via_json_load_into_tuple_from_local_file(file_path='[MASKED]')
    	"""
    import json
    try:
        data = json.load(s)
        first_layer_keys = list(data.keys())
        nested_keys = get_nested_keys(data)
        return (first_layer_keys, nested_keys)
    except Exception as e:
        return tuple() # {'error': str(e)}