def extract_Union_Pay_Card_Numbers_from_string_via_regex(obj):# error not working as pattern, missing re and also missing statement to return
    pattern =  r'622\d{13,16}|603601\d{10}|603265\d{10}|621977\d{10}|602969\d{10}|603708\d{10}|601428\d{10}|603367\d{10}|603694\d{10}'
     # Find all matches
    matches = re.findall(pattern, obj) 
    pass # return matches
#example usage:
#extract_Union_Pay_Card_Numbers_from_string_via_regex(text)
