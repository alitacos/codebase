def extract_tokens_via_regex(obj):# error not working regex pattern as it keeps some illegal chars like _-'" else works for other cases very good and missing import
    pattern =  r"(?![\d.!?])\w+"     # Find all matches
    pattern =  r"\b\w+(?:[-']\w+)*\b|[.,!?';]"     # Find all matches
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_tokens_via_regex(text)  
