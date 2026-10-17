def extract_HTML_elements_from_string_via_regex(obj): 
    pattern = r"""(?:<div.*?class=\"\w".*?>)(.*?)(?:<\\/\w*>)""" # Tag + class
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_HTML_elements_from_string_via_regex(text)
