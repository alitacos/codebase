def check_if_username_handler_exists_on_protonmail(target: str = '', allow_redirects: bool = True) -> dict:
    """
    Check if a ProtonMail username is available using ProtonMail's public API.

    Args:
        target (str): The ProtonMail username to check, e.g., 'exampleuser'.
        allow_redirects (bool): Whether HTTP redirects should be followed. Defaults to True.

    Returns:
        dict: A dictionary containing:
            - title (str | None): The <title> of the response page, if present.
            - status_code (int): The HTTP status code of the response (200 if exists, 404 if not).
            - raw (str): The response content with whitespace cleaned for easy parsing.
            - redirect (str): The final URL after any redirects.

    Notes:
        - A status code of 200 generally indicates the username exists or is available.
        - A status code of 404 generally indicates the username does not exist or is unavailable.
        - The 'raw' field contains the full text of the API response and can be used for debugging or logging.

    Example usage:
        >>> check_if_username_handler_exists_on_protonmail('testuser')
        {
            'title': None,
            'status_code': 200,
            'raw': '{"Available":true}',
            'redirect': 'https://account.protonmail.com/api/users/available?Name=testuser'
        }

        >>> check_if_username_handler_exists_on_protonmail('nonexistentuser123')
        {
            'title': None,
            'status_code': 404,
            'raw': '{"Available":false}',
            'redirect': 'https://account.protonmail.com/api/users/available?Name=nonexistentuser123'
        }
    """
    import requests
    from bs4 import BeautifulSoup
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    url=f"https://account.protonmail.com/api/users/available?Name={target}"
    r = requests.get(f"{url}", headers=headers, cookies=None, allow_redirects=allow_redirects)
    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]),'redirect':r.url}
