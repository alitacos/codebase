def extract_text_chunk_in_string_offsets_by_start_end_values(text=None,start='<title>',end='</title>'):
    try:
        if text.__class__ == bytes:
            text = text.decode('utf-8')
        else:
            text = str(text)
    except Exception as s:
        print(str(s))
        text = None
    try:
        _start = text.find(start) if text else None
        _end = text.find(end)  if text else None
        if _start != -1 and _end != -1 and _start !=None and  _end != None :
            chunk = text[_end + 7:_end]
            print(_start,_end)
            return chunk 
        else:
            return ''
            
    except Exception as e:
        print(str(e))
        return None
#example usage
#text = '''# <title> error not always working <title># works only for spesific patterns. if html has attributes, it </title> would lead to </title>false outputs'''
#extract_text_chunk_in_string_offsets_by_start_end_values(text=text,start='<title>',end='</title>')