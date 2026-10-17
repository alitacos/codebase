def extract_monero_crypto_addresses_via_regex(obj):# error not working regex pattern and missing import re returns NameError
    pattern =  r"4[0-9AB][123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{93}"
     # Find all matches
    matches = re.findall(pattern, obj) 
    pass # return matches
#example usage:
#extract_monero_crypto_addresses_via_regex(text)
