def open_archive_obj(path: str='') -> str:
    if path.endswith('.rar'):
        try:
            archive = rarfile.RarFile(path, mode='r')
            return archive
        except rarfile.BadRarFile:
            return None
    elif path.endswith('.zip'):
        try:
            archive = zipfile.ZipFile(path, mode='r')
            return archive
        except zipfile.BadZipFile:
            return 'None'