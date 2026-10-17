def check_if_username_handler_exists_on_wordpress(target:str='',allow_redirects:bool=True)->tuple:
    """
    Attempts to determine if a username exists on WordPress.com by performing
    an HTTP GET request to a constructed subdomain and extracting information
    from the response.

    The function does not guarantee existence detection; it simply requests
    "https://<target>.wordpress.com" and parses the page for visible content
    and the title.

    Args:
        target (str): Username used to construct the subdomain. (Defaults to '')
        allow_redirects (bool): Whether the request should follow HTTP redirects. (Defaults to True)

    Returns:
        dict: A dictionary containing:
            - title (str | None): Content of the <title> tag if present
            - status_code (int): HTTP response status code
            - raw (str | None): Cleaned visible text extracted from the HTML response
            - redirect (str): Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_wordpress(
        ...     target='example',
        ...     allow_redirects=True
        ... )
    """
    import requests
    from bs4 import BeautifulSoup
    
    url=f"https://{target}.wordpress.com"
    r = requests.get(f"{url}", headers=None, cookies=None, allow_redirects=allow_redirects)
    #if title is WordPress.com and in text {target}.wordpress.com doesn't\xa0exist, else you get the name of user and title of page
    #fuul_name, title = BeautifulSoup(r.text,'html.parser').find('title').get_text().split('|')###('Web2 Guide | Just another WordPress.com weblog'.split('|')

    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]) if BeautifulSoup(r.text,'html.parser') else None,'redirect':r.url}
#print(check_if_username_handler_exists_on_wordpress('tester'))#title': 'Web2 Guide | Just another WordPress.com weblog','status_code': 200,
#print(check_if_username_handler_exists_on_wordpress('papatoliosalex'))#'title': 'WordPress.com', 'status_code': 200
#works