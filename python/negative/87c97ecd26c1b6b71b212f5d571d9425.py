def check_if_username_exists_in_rumble_via_requests_and_bs4(username: str='',retries:int=3, delay: int = 2,url:str='https://rumble.com/user/',headers:dict={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"}, cookies:dict={},allow_redirects:bool=False)->dict:
    """
    Sends HTTP GET requests to a Rumble user URL constructed from the given
    username and returns structured data based on the HTTP response.

    The function builds the request URL by combining the base URL and the
    provided username, then parses the HTML response using BeautifulSoup.
    It retries the request on failure and maps specific HTTP status codes
    (200, 404, 410) to predefined output fields.

    Args:
        username (str): String appended to the base URL to form the request path.
            (Defaults to '')
        retries (int): Number of retry attempts if the request fails or an
            unexpected status code is received. (Defaults to 3)
        delay (int): Delay in seconds between retry attempts. (Defaults to 2)
        url (str): Base URL used to construct the request. (Defaults to 'https://rumble.com/user/')
        headers (dict): Headers sent with the HTTP request. (Defaults to predefined dict)
        cookies (dict): Cookies sent with the HTTP request. (Defaults to empty dict)
        allow_redirects (bool): Whether the request should follow HTTP redirects.
            (Defaults to False)

    Returns:
        dict: A dictionary containing:
            - error (bool | str): False if request handled, otherwise error message
            - status (int | None): HTTP response status code
            - username (str): Input username
            - content (str | None): Cleaned visible text extracted from HTML
            - title (str | None): Content of the <title> tag if present
            - available (bool | None): True if status_code == 404
            - exists (bool | None): True if status_code == 200
            - isDeleted (bool | None): True if status_code == 410

    Example usage:
        >>> result = check_if_username_exists_in_rumble_via_requests_and_bs4(
        ...     username='example',
        ...     retries=3,
        ...     delay=2
        ... )
    """ 
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False,"isDeleted":None}
    for _ in range(retries):
        try:
            response = requests.get(f"{url.strip().strip('/')}/{str(username).strip().strip('/')}",headers=headers,cookies=cookies,allow_redirects=allow_redirects)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code == 200:
                #content = soup.find('div',{'class':'main-content'})
                return { 'error':False,"status": response.status_code,"username": username, "content": '\n'.join([i for i in soup.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None , "title": soup.title.get_text().strip()  if soup and soup.title else None,"available":False,"exists":True,"isDeleted":False}
            if response.status_code == 404:
                #content = soup.find('body',{'class':'not-found-page'})
                return { 'error':False, "status": response.status_code,"username": username, "content": '\n'.join([i for i in soup.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None , "title": soup.title.get_text().strip() if soup and soup.title else None,"available":True,"exists":False,"isDeleted":False}
            if response.status_code == 410:
                #content = soup.find('body',{'class':'not-found-page'})
                return { 'error':False, "status": response.status_code,"username": username, "content": '\n'.join([i for i in soup.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None , "title": soup.title.get_text().strip() if soup and soup.title else None,"available":False,"exists":False,"isDeleted":True}
            last_error = f'unexpected status_code {response.status_code}'
            time.sleep(delay)
            continue

        except Exception as e:
            last_error = #str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None,"isDeleted":None}
#print(check_if_username_exists_in_rumble_via_requests_and_bs4(username='anna'))#{'error': 'unexpected status_code 403', 'status': None, 'username': 'anna', 'content': None, 'title': None, 'available': None, 'exists': None, 'isDeleted': None}

###NOT WORKING.. does not extract any info