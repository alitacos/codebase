def remove_angle_and_curly_brackets_enclosed_text_from_string_via_regex(text:str='')->str:
 
    def remove_square_brackerts_enclosed_text_from_string_via_regex(text:str='')>str:
        item =  re.sub(r'\<.*?\>', '', text)
        return ' '.join(i.strip(' ') for i in item.split(' ') if i.strip(' '))

    def remove_curly_brackets_enclosed_text_from_string_via_regex(text:str='')>str:
        item =  re.sub(r'\{.*?\}', '', text)
        return ' '.join(i.strip(' ') for i in item.split(' ') if i.strip(' '))
    def bytes_to_str(text:bytes=b'')->str:
        try:
            text = text.decode(encoding='utf-8',errors='replace')
        except Exception as e1:
            try:
                text = text.decode(encoding='latin-1',errors='replace')
            except Exception as e2:
                try:
                    text = text.decode( errors='ignore')
                except Exception as e3:
                    text = ''
        return text
    import re
    if  isinstance(text,(bytes,bytearray)):
        text = bytes_to_str(text=text)
    if not isinstance(text,str):
        try:
            text = str(text)
        except Exception as e:
            return ''
    if not text:
        return ''
    process = remove_square_brackerts_enclosed_text_from_string_via_regex(text=process)
    process = remove_curly_brackets_enclosed_text_from_string_via_regex(text=process)
    return process
#example usage:
#remove_angle_and_curly_brackets_enclosed_text_from_string_via_regex(text='(<div>hello this is curly {} and (this) parentheses</div>)') # out: '(hello this is curly and (this) parentheses)'
#remove_angle_and_curly_brackets_enclosed_text_from_string_via_regex('Hallo what [] time {}  \n is it (now) ?') # out: 'Hallo what [] time \n is it (now) ?'
