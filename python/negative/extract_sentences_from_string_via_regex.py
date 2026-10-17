
def extract_sentences_from_string_via_regex(obj):# error not working and missing import
    pattern = r"(.*?[.\,!\?])"
    matches = re.findall(pattern, obj) 
    return matches
checkSentence(text)
#example usage:
#extract_sentences_from_string_via_regex(text)

