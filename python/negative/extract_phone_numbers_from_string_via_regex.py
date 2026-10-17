# error not working code . patterns are not valid as expected
def extract_phone_numbers_from_string_via_regex(obj: str) -> list:
    import re
    #pattern = r"\+[\d{1,3, ,-}?]*|00[\d{1,3, ,-}?]*" # ok for simple numbers. checks not for letters
    #pattern = r"\+[\d\{1,3, ,-}(\), ,-]*|00[\d\{1,3, ,-}(\), ,-]*" # strings text, are extracted too
    pattern = r"\+[\d\{1,3, ,-}(\)]*|00[\d\{1,3, ,-}(\), ,-]*" # strings text, are extracted too 
    matches = re.findall(pattern, obj)  

    return matches
#extract_phone_numbers_from_string_via_regex('+49 1768989o878+30 176898h9878 +1 (555)-432-3432     store the requests as raw html files,json or else . we use it temporarely until we deside how we use our dataset at end.  reuse file for exact requests')
