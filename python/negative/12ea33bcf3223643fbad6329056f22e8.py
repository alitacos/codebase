def bytes_to_str(text: bytes='')->str:
    try:    
        try:
            text = text.decode(encoding='utf-8', errors='replace')
        except Exception as e1:
            try:
                text = text.decode(encoding='latin-1', errors='replace')
            except Exception as e2:
                try:
                    text = text.decode(errors='ignore')
                except Exception as e3:
                    text = ''
        return text
    except Exception as e:
        #print(e)
        return ''