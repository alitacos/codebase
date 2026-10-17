def extract_password_strings_via_regex(obj):# error not working regex pattern and missing import re returns NameError
    pattern = r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&\_])[\S+\!\?\.,]{8,}'# error not working
    pattern = r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&\_])[A-Za-z\d@#$%&\_]{8,}$'# error not working # 8 at end is the length of the token
    matches = re.findall(pattern, obj) 
    return matches
#example usage:
#extract_password_strings_via_regex(text)
