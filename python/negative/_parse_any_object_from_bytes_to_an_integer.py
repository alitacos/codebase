def parse_any_object_from_bytes_to_an_integer(b=None):  # not working as expected. it only parses bytes, but no other types. 
    try:
        return int.from_bytes(b,"big" )
    except Exception as e:
        #print(str(e))
        return None
#example usage:
#parse_any_object_from_bytes_to_an_integer(b=None)#out: None # is not parsed
#parse_any_object_from_bytes_to_an_integer(b=49)#out: None # is not parsed
#parse_any_object_from_bytes_to_an_integer(b=b'49')#out: 13369 # is   parsed