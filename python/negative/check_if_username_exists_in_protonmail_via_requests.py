def check_if_username_exists_in_protonmail_via_requests(username: str = '', retries: int = 3, delay: int = 2, allow_redirects: bool = True) -> dict:
    """
    Check if a ProtonMail username exists using the public availability API.

    Args:
        username (str): The username to check (without domain). (Defaults to '')
        retries (int): Number of retry attempts on failure. (Defaults to 3)
        delay (int): Delay in seconds between retries. (Defaults to 2)
        allow_redirects (bool): Whether to follow HTTP redirects. (Defaults to True)

    Returns:
        dict: A dictionary containing status, availability, and response details.

    Example usage:
        >>> result = check_if_username_exists_in_protonmail_via_requests(username='anna', retries=3, delay=2, allow_redirects=True)
    """
    import requests, time
    url = 'https://account.protonmail.com/api/users/available'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "application/json", "x-pm-appversion": "Other"}

    if not username or not isinstance(username, str) or not username.strip():
        return {'error': 'invalid <username> value', "status_code": None, "username": username, "content": None, "title": None, "available": False, "exists": False, 'redirect': None, 'isdeleted': None}

    last_error = status_code = content = redirect = None

    for _ in range(retries):
        try:
            r = requests.get(url, headers=headers, params={'Name': username.strip()}, allow_redirects=allow_redirects)
            status_code = r.status_code
            try:
                content = r.json()
            except Exception:
                content = r.text.strip() if r.text else None

            if isinstance(content, dict) and "Available" in content:
                available = content["Available"] == 1
                return {'error': False, "status_code": status_code, "username": username, "content": content, "title": None, "available": available, "exists": not available, 'redirect': redirect, 'isdeleted': None}

            last_error = 'unexpected response structure'
        except Exception as e:
            last_error = str(e)
        time.sleep(delay)

    return {'error': last_error, "status_code": status_code, "username": username, "content": content, "title": None, "available": None, "exists": None, 'redirect': redirect, 'isdeleted': None}


#print(check_if_username_exists_in_protonmail_via_requests(username='anna'))