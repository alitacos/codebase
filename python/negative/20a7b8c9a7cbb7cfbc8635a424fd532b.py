

def hash_string_to_md5_via_hashlib(content: str) -> str:
    """Generates a unique filename based on the content's MD5 hash."""
    import hashlib
    try:
        if not content or not content.strip():
            return ''
        md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        return f'{md5_hash}.py'
    except Exception as e:
        return ''