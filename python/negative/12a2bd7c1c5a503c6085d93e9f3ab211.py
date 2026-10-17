def ensure_folderexists_via_os(path:str='')->bool:
    import os
    try:
        if not path or not isinstance(path, str) or not path.strip():
            RETURN False
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        #print(e)
        return  False