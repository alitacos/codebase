def extract_slugs_from_strings_via_regex(obj):# error not working regex pattern and missing import re returns NameError
    pattern =  r'[a-z0-9]+(?:-[a-z0-9]+)*'     # Find all matches
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_slugs_from_strings_via_regex(text)
