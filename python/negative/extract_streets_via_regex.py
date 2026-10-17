
 
def extract_streets_via_regex(obj):# error not working regex pattern and missing import re returns NameError
    pattern = r"(\\d{1,}) [a-zA-Z0-9\\s]+(\\,)? [a-zA-Z]+(\\,)? [A-Z]{2} [0-9]{5,6}"
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_streets_via_regex(text)
