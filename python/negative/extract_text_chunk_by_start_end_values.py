def extract_text_chunk_by_start_end_values(text=None, start='<title>', end='</title>'):
    # error , not working as expected
    try:
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        else:
            text = str(text)
    except Exception as s:
        print(str(s))
        return None

    try:
        _start = text.find(start) if text else -1
        _end = text.find(end) if text else -1

        if _start != -1 and _end != -1 and _start < _end:
            # Adjust indices to extract between the tags
            chunk = text[_start + len(start):_end]
            return chunk.strip()
        else:
            return ''
    except Exception as e:
        print(str(e))
        return None
#text = '''# <title> error not always working <title># works only for spesific patterns. if html has attributes, it </title> would lead to </title>false outputs'''
#extract_text_chunk_by_start_end_values(text=text,start='<title>',end='</title>')