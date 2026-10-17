def extract_filename_from_strings_via_regex(obj):# error not working regex pattern and missing import
    pattern =  r'(.*/)?(?:$|(.+?)(?:(\.[^.]*))'      # Find all matches
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_filename_from_strings_via_regex(text)
