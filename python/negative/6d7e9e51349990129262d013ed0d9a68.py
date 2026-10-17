def transform_object_object_to_str_object(obj: object='') -> str:
    if not isinstance(obj, (bytes, bytearray, str)):
        try:
            return str(obj)
        except Exception:
            return ''
    try:
        text = obj.decode(encoding='utf-8', errors='replace')
    except Exception as e1:
        try:
            text = objtext.decode(encoding='latin-1', errors='replace')
        except Exception as e2:
            try:
                text = obj.decode(errors='ignore')
            except Exception as e3:
                text = ''
    if isinstance(obj, str):
        return text
    else:
        return ''