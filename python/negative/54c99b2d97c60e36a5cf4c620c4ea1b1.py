def check_if_email_exists_on_pinterest_via_requests_and_related_data_in_dict(email: str = '', retries:int=3, delay:int=2, url : str = "https://de.pinterest.com/resource/ApiResource/get/",headers : dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36","X-Pinterest-Source-Url":"/password/reset/","Accept": "application/json, text/javascript, */*; q=0.01","Referer": "https://de.pinterest.com/","X-Requested-With": "XMLHttpRequest","X-Pinterest-AppState": "active","X-Pinterest-PWS-Handler": "www/password/reset.js","X-App-Version": "d8c18cb",},cookies:dict=  {"csrftoken": "0538a04e1f481bb0c00141c16c159970"},allow_redirects:bool=False)  -> dict:
    """
    Sends HTTP GET requests to a Pinterest API endpoint using the provided
    email and returns the JSON response along with additional metadata.

    The function constructs query parameters containing the email, performs
    the request with the given headers and cookies, and returns the parsed
    JSON response if the status code is 200. It retries the request on failure.

    Args:
        email (str): String included in the request payload. Must contain '@'
            to pass basic validation. (Defaults to '')
        retries (int): Number of retry attempts if the request fails or returns
            a non-200 status code. (Defaults to 3)
        delay (int): Delay in seconds between retry attempts. (Defaults to 2)
        url (str): Endpoint used for the HTTP request. (Defaults to
            'https://de.pinterest.com/resource/ApiResource/get/')
        headers (dict): Headers sent with the HTTP request. (Defaults to predefined dict)
        cookies (dict): Cookies sent with the HTTP request. (Defaults to predefined dict)
        allow_redirects (bool): Whether the request should follow HTTP redirects.
            (Defaults to False)

    Returns:
        dict: A dictionary containing either:
            - Parsed JSON response extended with:
                - error (bool): False when status_code == 200
                - status (int): HTTP status code (200)
            - OR fallback dictionary:
                - error (bool | str): Error flag or message
                - status (int | None): HTTP status code or None

    Example usage:
        >>> result = check_if_email_exists_on_pinterest_via_requests_and_related_data_in_dict(
        ...     email='example@email.com',
        ...     retries=3,
        ...     delay=2
        ... )
    """  
    import requests
    import json
    if not email or not isinstance(email, str) or not str(email).strip() or not '@' in str(email):
        return  {'error':'missing or invalid <email>', 'status':None}
    for _ in range(retries):
        try:
            query_params = {"source_url": "/password/reset/","data": json.dumps({"options": {"url": "/v3/register/exists/","data": {"email": str(email).strip() }},"context": {}}),"_": "1750075105176"}
            response = requests.get(url, headers=headers, cookies=cookies, params=query_params,allow_redirects=allow_redirects)
            if response.status_code == 200:
                out = response.json()
                out['error'] = False
                out['status'] = 200
                return out
            last_error = False if response.status_code == 200 else True
            status = response.status_code
            continue
        except Exception as e:
            last_error = str(e)
            status = None
    return  {'error':last_error, 'status':status}

#example usage:
#print(check_if_email_exists_on_pinterest_via_requests_and_related_data_in_dict('alitakos90ddd@grr.laa'))
# NOT WORKING. returns some dictionary that does not include any usefull information 