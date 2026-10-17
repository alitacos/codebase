import rarfile
import zipfile

def get_file_raw_content_string_from_archive_file(archive: str | rarfile.RarFile | zipfile.ZipFile = '',member: str = '',passwords:list|str=None) -> str:
    """
    Extracts the raw content of a specified file (member) from a ZIP or RAR archive.
    Accepts either a file path or an already opened archive object, and optionally
    attempts password-based extraction for protected files.

    Args:
        archive (str | rarfile.RarFile | zipfile.ZipFile): Path to the archive file
            or an already opened archive object (ZIP or RAR). Defaults to ''.
        member (str): The name or path of the file داخل the archive to extract. Defaults to ''.
        passwords (list | str): A single password or a list of passwords to try if
            the archive member is encrypted. Defaults to None.

    Returns:
        str: The raw file content as string if successfully extracted.
            Returns an empty string ('') if extraction fails, the archive is invalid,
            or no correct password is found.

    Example usage:
        >>> result = get_file_content_string_from_archive_file(archive='data.zip',member='log.txt',  passwords=['1234', 'secret']  )
    """
    def requires_password(archive, member) -> bool:
        """
        Determines whether a specific file (member) داخل an archive requires a password
        for extraction. Supports ZIP and RAR archive formats.
    
        Args:
            archive (Any): An opened archive object (e.g., zipfile.ZipFile or
                rarfile.RarFile).
            member (Any): The name/path of the file داخل the archive to check.
    
        Returns:
            bool: True if the specified member requires a password, otherwise False.
    
        Example usage:
            >>> result = requires_password(archive=my_archive, member='file.txt')
        """
        info = archive.getinfo(member)

        if isinstance(archive, zipfile.ZipFile):
            return (info.flag_bits & 0x1) != 0

        if isinstance(archive, rarfile.RarFile):
            return info.needs_password() if hasattr(info, "needs_password") else False

        return False

    def normalize_password(pwd) -> bytes | None:
        """
        Normalizes a password input into a bytes object suitable for archive
        extraction functions. Handles strings and bytes, returning None for
        unsupported types.
    
        Args:
            pwd (Any): The password input, which can be a string, bytes, or None.
    
        Returns:
            bytes | None: The password encoded as UTF-8 bytes if input is a string,
                returned as-is if already bytes, or None if input is None or an
                unsupported type.
    
        Example usage:
            >>> result = normalize_password(pwd='secret123')
        """
        if pwd is None:
            return None
        if isinstance(pwd, bytes):
            return pwd
        if isinstance(pwd, str):
            return pwd.encode('utf-8')
        return None
    if isinstance(archive, str):
        if archive.lower().endswith('.rar'):
            archive = rarfile.RarFile(archive)
        elif archive.lower().endswith('.zip'):
            archive = zipfile.ZipFile(archive)
    if not isinstance(archive, (rarfile.RarFile, zipfile.ZipFile)):
        return ''
    content = None
    if member:
        try:
            content = archive.read(member)
        except Exception:
            content = None
    if member and passwords and content is None:
        if not requires_password(archive, member):
            return ''  # or keep content=None and exit
        if isinstance(passwords, (str, bytes)):
            passwords = [passwords]
        for password in passwords:
            pwd = normalize_password(password)
            try:
                content = archive.read(member, pwd=pwd)
            except Exception:
                content = None
            if content is not None:
                break
    if content is None:
        return ''
    return content