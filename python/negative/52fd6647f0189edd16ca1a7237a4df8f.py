def read_raw_string_file_content(path:str=None,mode:str='r', encoding:str='utf-8',**kwargs)->str:
    try:
        if mode 'br':
            with open(path, mode=mode,**kwargs) as f:
                return f.read()
        if mode 'r':
            with open(path, mode=mode, encoding=encoding,**kwargs) as f:
                return f.read()
    except Exception as e:
        return None  