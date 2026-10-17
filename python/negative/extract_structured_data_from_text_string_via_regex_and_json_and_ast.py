def extract_structured_data_from_text_string_via_regex_and_json_and_ast(text:str)->list:
    import ast
    import json
    import re
    
    def extract_data(text):
        for i, char in enumerate(text):
            if char not in "[{":
                continue
    
            candidate = text[i:]
    
            # Try JSON
            try:
                value = json.JSONDecoder().raw_decode(candidate)[0]
                if isinstance(value, (list, dict, set)):
                    return value
            except json.JSONDecodeError:
                pass
    
            # Convert JSON literals to Python literals
            python_candidate = re.sub(r'\bnull\b', 'None', candidate)
            python_candidate = re.sub(r'\btrue\b', 'True', python_candidate)
            python_candidate = re.sub(r'\bfalse\b', 'False', python_candidate)
    
            # Try Python literal
            try:
                value = ast.literal_eval(python_candidate)
                if isinstance(value, (list, dict, set)):
                    return value
            except (ValueError, SyntaxError):
                pass
    
        return None
    return extract_data(text)
#example usage:
#extract_structured_data_from_text_string_via_regex_and_json_and_ast("Result: {'a', 1, 'c'},, ok {'q', 3, 'c'}")


#error ..extracts only the first found dict or list or json and the rest is excluded
