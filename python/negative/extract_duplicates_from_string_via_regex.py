def extract_duplicates_from_string_via_regex(obj):# error not working
    pattern = r"\b(\w+)\b(?=.*\b\1\b)"
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_duplicates_from_string_via_regex(text)
