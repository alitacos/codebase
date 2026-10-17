def check_if_username_handler_exists_on_codecademy(target:str='',allow_redirects:bool=True )->tuple:
    """
    Sends an HTTP GET request to a Codecademy user page and parses the HTML 
    title and page content. Returns metadata about the request.

    Note: This function does not reliably detect whether a username exists.
    Codecademy returns a 404 page for non-existent or inaccessible user URLs.

    Args:
        target (str): Username string to check. (Defaults to '')
        allow_redirects (bool): Whether HTTP redirects should be followed. (Defaults to True)

    Returns:
        dict: Dictionary containing:
            - title (str | None): Text from the <title> tag of the response, if available.
            - status_code (int): HTTP status code of the response.
            - raw (str | None): Cleaned text content of the page.
            - redirect (str): Final URL after any redirects.

    Example usage:
        >>> result = check_if_username_handler_exists_on_codecademy(target='exampleuser', allow_redirects=True)
    """
    import requests
    from bs4 import BeautifulSoup
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    url=f"https://www.codecademy.com/{target}"
    r = requests.get(f"{url}", headers=headers, cookies=None, allow_redirects=allow_redirects)
    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]),'redirect':r.url}
#print(check_if_username_handler_exists_on_codecademy('anonymous'))# {'title': 'Page Not Found | Codecademy', 'status_code': 404, 'raw': 'Page Not Found | Codecademy', 'redirect': 'https://www.codecademy.com/@anonymous'}
#print(check_if_username_handler_exists_on_codecademy('anna'))# {'title': 'Page Not Found | Codecademy', 'status_code': 404, 'raw': 'Page Not Found | Codecademy', 'redirect': 'https://www.codecademy.com/@anna'}
#NOT WORKING. ALWAYS RETURNS THE SAME STATUS CODE and TITLE 'title': 'Page Not Found | Codecademy', 'status_code': 404,