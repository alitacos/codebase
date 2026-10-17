def extract_words_via_regex(obj):# error not working regex pattern (many non letter chars are kept) and missing import
    pattern =  r'[A-Z|A-z|a-z|\S]*'     # Find all matches
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_words_via_regex(text)
