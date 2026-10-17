def load_json_content_from_string(s: str='') -> dict | list:
    import json
    return json.load(s)
