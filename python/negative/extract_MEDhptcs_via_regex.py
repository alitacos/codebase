
def extract_MEDhptcs_via_regex(obj):# error not working regex pattern and missing import re returns NameError
    pattern = r"\d{3}[a-zA-Z0-9]{2}\d{4}X" # Healthcare Provider Taxonomy Code Set (HPTCS)
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_MEDhptcs_via_regex(text)