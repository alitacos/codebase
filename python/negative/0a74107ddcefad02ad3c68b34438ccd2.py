def check_if_username_handler_exists_on_bitbucket(target:str='',allow_redirects:bool=True )->tuple:
    """
    Performs an HTTP GET request to a Bitbucket user page constructed from the
    given username and returns parsed information from the response.

    The input string is directly inserted into the URL "https://bitbucket.org/<target>"
    without validation. The function does not guarantee that the user exists;
    it only retrieves the page content and metadata.

    Args:
        target (str): Username to insert into the Bitbucket URL. (Defaults to '')
        allow_redirects (bool): Whether the request should follow HTTP redirects. (Defaults to True)

    Returns:
        dict: A dictionary containing:
            - title (str | None): Content of the <title> tag if present
            - status_code (int): HTTP response status code
            - raw (str): Cleaned visible text extracted from the HTML response
            - redirect (str): Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_bitbucket(
        ...     target='example',
        ...     allow_redirects=True
        ... )
    """
    import requests
    from bs4 import BeautifulSoup
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    url=f"https://bitbucket.org/{target}"
    r = requests.get(f"{url}", headers=headers, cookies=None, allow_redirects=allow_redirects)
    #titles contain the string '- Profile | Pinterest' if user exists else is empty
    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]),'redirect':r.url}
##works via status code
#print(check_if_username_handler_exists_on_bitbucket('test'))#{'title': 'Bitbucket', 'status_code': 200, 'raw': 'Bitbucket', 'redirect': 'https://bitbucket.org/Test/workspace/repositories/'}
#print(check_if_username_handler_exists_on_bitbucket('anonymous'))# {'title': '404 — Bitbucket', 'status_code': 404, 'raw': '404 — BitbucketResource not foundReturn to the previous page orgo back to your dashboard.Log in', 'redirect': 'https://bitbucket.org/anonymous/'}
##WORKS