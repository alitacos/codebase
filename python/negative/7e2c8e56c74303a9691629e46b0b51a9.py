def get_nested_json_keys_from_local_file(file_path: str='') -> list:
    """
    Retrieve all keys from a nested JSON  local file.

    This function reads a JSON file from the given file path and extracts all keys
    from the nested JSON structure. It handles both dictionaries and lists.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - list: A list of all keys in the nested JSON structure.
    """
    import json
    with open(file_path, 'r') as f:
        data = json.load(f)
    keys = []
    if isinstance(data, dict):
        for key, value in data.items():
            keys.append(key)
            if isinstance(value, (dict, list)):
                keys.extend(get_nested_keys(value))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                keys.extend(get_nested_keys(item))
    return keys