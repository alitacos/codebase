import zipfile
import rarfile
def get_content_of_archive_member_as_string_and_bytes( archive:rarfile.RarFile|zipfile.ZipFile|str|bytes=None, member:str='',passwords : list =[])->tuple:
    """
    Extract a file from a ZIP or RAR archive and return its raw bytes and decoded string content.

    The function supports:
    - ZIP files (zipfile.ZipFile or .zip path)
    - RAR files (rarfile.RarFile or .rar path)
    - Archive provided as file path (str)
    - Archive provided as raw bytes (attempts decoding as path string)

    It attempts to read the file:
    - Without password first
    - Then with a list of provided passwords (if needed)

    Args:
        archive (rarfile.RarFile | zipfile.ZipFile | str | bytes):
            Archive object, file path, or raw bytes representing a path.
        member (str):
            Path/name of the file inside the archive to extract.
        passwords (list):
            List of passwords to try if archive member is encrypted.
            Can also be a single string (will be normalized internally).

    Returns:
        tuple:
            (raw_bytes, decoded_string)
            - raw_bytes (bytes): original file content in bytes (or b'' if failed)
            - decoded_string (str): UTF-8 decoded content (errors ignored), or ""

    Example usage:
        >>> result = get_content_of_archive_member_in_string_and_bytes(archive="data.zip",member="file.txt",passwords=["1234", "admin"])
    """


    def open_archive(archive: str = '' )->rarfile.RarFile|zipfile.ZipFile|None:
        """Open archive from file path and return appropriate archive object."""
        if not archive:
            return None
        try:
            if archive.endswith('.zip'):
                return zipfile.ZipFile(archive, 'r')
            elif archive.endswith('.rar'):
                return rarfile.RarFile(archive)
            else:
                return None
        except Exception as e:
            return None
    def ensure_archive_object(archive:rarfile.RarFile|zipfile.ZipFile|str|bytes=None, member:str='')   ->rarfile.RarFile|zipfile.ZipFile|None:   
        #import rarfile
        #import zipfile
        if not archive or not member:
            return None    
        if not isinstance(archive, (rarfile.RarFile,zipfile.ZipFile)):
            if isinstance(archive,str):
                archive = open_archive(archive)
            elif isinstance(archive,bytes):
                try:
                    archive = open_archive(archive.decode('utf-8'))
                  
                except UnicodeDecodeError:
                    archive = open_archive(archive.decode('latin-1'))  # fallback
                except Exception:
                    archive = None
            else:
                archive = None
        return archive
 
    def rar_raw_content_bytes(archive, member, passwords=None) -> bytes:
        """
        Extract raw bytes from RAR archive.

        NOTE: rarfile typically uses `open()` rather than `read()` for file objects.
        """
        #import rarfile
        passwords = passwords or []
        try:
            with archive.read(member) as content:
                return content
        except Exception:
            pass
        if passwords:          
            for pwd in passwords:
                try:
                    with archive.read(member, pwd=pwd) as content:
                        return content
                except Exception:
                    continue
        return b''
      
    def zip_raw_content_bytes(archive, member, passwords=None) -> bytes:
        import zipfile  
        passwords = passwords or []
        try:
            with archive.read(member) as content:
                return content
        except Exception:
            pass
        if passwords:
            for pwd in passwords:
                try:
                    with archive.read(member, pwd=bytes(pwd, "utf-8")) as content:
                        return content
                except Exception:
                    continue
        return b''

    def rar_content_string(archive, member, passwords=None) -> str:
        import rarfile   
        passwords = passwords or []
        try:
            with archive.open(member) as f:
                content = f.read()
                return content.decode("utf-8", errors="ignore") if isinstance(content, (bytes, bytearray)) else content
        except Exception:
            pass
        if passwords:
            for pwd in passwords:
                try:
                    with archive.open(member, pwd=pwd) as f:
                        content = f.read()
                        return content.decode("utf-8", errors="ignore") if isinstance(content, (bytes, bytearray)) else content
                except Exception:
                    continue  
        return ""

    def zip_content_string(archive, member, passwords=None) -> str:
        import zipfile
        passwords = passwords or []  
        # normal case
        try:
            with archive.open(member) as f:
                content = f.read()
                return content.decode("utf-8", errors="ignore") if isinstance(content, (bytes, bytearray)) else content
        except Exception:
            pass   
        if passwords:
            for pwd in passwords:
                try:
                    with archive.open(member, pwd=bytes(pwd, "utf-8")) as f:
                        content =  f.read()
                        return content.decode("utf-8", errors="ignore") if isinstance(content, (bytes, bytearray)) else content
                except Exception:
                    continue
        return ""



      
    passwords  = [passwords] if isinstance(passwords, str) else passwords or []
    archive = ensure_archive_object(archive=archive, member=member)  

      
    if isinstance(archive, rarfile.RarFile):
        raw=  rar_raw_content_bytes(archive=archive, member=member, passwords=passwords)
        string= rar_content_string(archive=archive, member=member, passwords=passwords)
        return raw, string

    
    elif isinstance(archive, zipfile.ZipFile):
        raw=  zip_raw_content_bytes(archive=archive, member=member, passwords=passwords)
        string= zip_content_string(archive=archive, member=member, passwords=passwords)
        return raw, string
    return None, None