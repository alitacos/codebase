def extract_XML_from_string_via_regex(obj): 
    pattern = r"(?:<from.*?>)(.*?)(?:<\\/from>)"
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_XML_from_string_via_regex(text)
