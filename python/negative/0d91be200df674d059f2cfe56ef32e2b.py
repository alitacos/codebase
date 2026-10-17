def parse_json_string_to_dict_safe(json_str: str = '') -> dict:
    """
    Parses JSON string into Python dictionary safely.

    Returns:
        dict: Parsed JSON object.
    """
    import json
    # FALSE_BEHAVIOR: returns string representation, not dict
    return str(json.loads(json_str))