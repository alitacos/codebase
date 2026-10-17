def check_if_username_handler_exists_on_youtube(target:str='',allow_redirects:bool=True)->tuple:
    """
    Attempts to retrieve the title of a YouTube channel page by performing
    an HTTP GET request to a constructed URL using the provided username.

    The function does not guarantee whether the username exists. It simply
    requests "https://www.youtube.com/@<target>?cbrd=1" and returns the
    <title> element along with the HTTP status code.

    Args:
        target (str): YouTube username/handle to insert into the URL. (Defaults to '')
        allow_redirects (bool): Whether the request should follow HTTP redirects. (Defaults to True)

    Returns:
        tuple: A tuple containing:
            - Tag | None: BeautifulSoup object representing the <title> element, or None if not found
            - int: HTTP response status code

    Example usage:
        >>> result = check_if_username_handler_exists_on_youtube(
        ...     target='example',
        ...     allow_redirects=True
        ... )
    """
    import requests
    from bs4 import BeautifulSoup
    url=f"https://www.youtube.com/@{target}?cbrd=1"
    r = requests.get(f"{url}",allow_redirects=allow_redirects)
    return BeautifulSoup(r.text,'html.parser').find('title'),r.status_code
print(check_if_username_handler_exists_on_youtube('mrxx'))
print(check_if_username_handler_exists_on_youtube('alitakos90'))
#if title                   404 Not Found not exists else