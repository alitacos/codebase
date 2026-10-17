def extract_base64_strings_via_regex(obj):# error not working regex pattern and missing import re returns NameError
    pattern = r'(?:[A-Z0-9+/]{4})*(?:[A-Z0-9+/]{2}(?:==|=)?|[A-Z0-9+/]{3})'
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#check_if_string_is_base64(text)