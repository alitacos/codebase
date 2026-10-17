def check_if_username_handler_exists_on_twitter(target:str='',allow_redirects=True)->tuple:
    """
    Checks whether a given Twitter/X username (handle) exists by querying
    an external lookup service.

    The function sends a POST request with the provided username to a third-party
    endpoint and returns the raw response text along with the final URL after
    any redirects. The response can be inspected to determine if the username
    is valid or already taken.

    Args:
        target (str): The Twitter/X username (without '@') to check. (Defaults to '')
        allow_redirects (Any): Whether to follow HTTP redirects during the request. (Defaults to True)

    Returns:
        tuple: A tuple containing:
            - str: Raw response text from the lookup service
            - str: Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_twitter(target='username', allow_redirects=True)
    """
    import requests
    inp = {"input": target}
    header = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",              "x-requested-with": "XMLHttpRequest"}
    r = requests.post(f"https://tweeterid.com/ajax.php", data=inp, headers=header,allow_redirects=allow_redirects)

    return r.text,r.url
#print(check_if_username_handler_exists_on_twitter('anonymous'))
#print(check_if_username_handler_exists_on_twitter('alitakospapatolios'))
#print(check_if_username_handler_exists_on_twitter('anna'))
####false url