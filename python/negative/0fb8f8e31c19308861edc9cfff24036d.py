def check_if_username_handler_exists_on_cashme(target:str='',allow_redirects:bool=True )->tuple:
    """
    Performs an HTTP GET request to a Cash App (cash.me) page constructed from
    the given username and returns parsed information from the response.

    The input string is directly inserted into the URL "https://cash.me/<target>"
    without validation. The function does not guarantee that the username exists;
    it only retrieves the page content and metadata.

    Args:
        target (str): String inserted into the Cash App URL. (Defaults to '')
        allow_redirects (bool): Whether the request should follow HTTP redirects. (Defaults to True)

    Returns:
        dict: A dictionary containing:
            - title (str | None): Content of the <title> tag if present
            - status_code (int): HTTP response status code
            - raw (str): Cleaned visible text extracted from the HTML response
            - redirect (str): Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_cashme(
        ...     target='example',
        ...     allow_redirects=True
        ... )
    """
    import requests
    from bs4 import BeautifulSoup
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    url=f"https://cash.me/{target}"
    r = requests.get(f"{url}", headers=headers, cookies=None, allow_redirects=allow_redirects)
    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]),'redirect':r.url}
##works via status code
#print(check_if_username_handler_exists_on_cashme('test'))# {'title': 'Pay $test on Cash App', 'status_code': 200, 'raw': 'Pay $test on Cash App', 'redirect': 'https://cash.app/$test'}
#print(check_if_username_handler_exists_on_cashme('alitajsksdbdsibhhsduwjnwnnwnwjk'))# {'title': None, 'status_code': 404, 'raw': '{"success":false,"message":{"message":"","alreadyLocalized":true},"debugInfo":""}', 'redirect': 'https://cash.app/$alitajsksdbdsibhhsduwjnwnnwnwjk'} 
 #works