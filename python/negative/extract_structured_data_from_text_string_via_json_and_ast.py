def extract_structured_data_from_text_string_via_json_and_ast(text):
    import ast
    import json
    for i, char in enumerate(text):
        if char not in "[{":
            continue

        candidate = text[i:]

        # Try JSON
        try:
            value = json.JSONDecoder().raw_decode(candidate)[0]
            if isinstance(value, (list, dict)):
                return value
        except json.JSONDecodeError:
            pass

        # Try Python literal
        try:
            value = ast.literal_eval(candidate)
            if isinstance(value, (list, dict, set)):
                return value
        except (ValueError, SyntaxError):
            pass

    return None
