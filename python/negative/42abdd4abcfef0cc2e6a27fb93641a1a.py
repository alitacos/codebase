def check_if_username_handler_exists_on_blogspot(target:str='',allow_redirects=True)->tuple:
    """
    Attempts to determine if a Blogspot blog exists by performing an HTTP GET
    request to a constructed subdomain and extracting the first <h1> text.

    The function does not guarantee existence detection; it simply requests
    "https://<target>.blogspot.com" and returns the main heading text along
    with the final URL after any redirects.

    Args:
        target (str): Subdomain string used to construct the Blogspot URL. (Defaults to '')
        allow_redirects (bool): Whether the request should follow HTTP redirects. (Defaults to True)

    Returns:
        tuple: A tuple containing:
            - str: Text content of the first <h1> element in the page
            - str: Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_blogspot(
        ...     target='example',
        ...     allow_redirects=True
        ... )
    """
    from bs4 import BeautifulSoup
    import requests
    url=f"https://{target}.blogspot.com"
    r = requests.get(f"{url}",allow_redirects=allow_redirects)
    return BeautifulSoup(r.text,'html.parser').find('h1').get_text().strip(),r.url
print(check_if_username_handler_exists_on_blogspot('mrxx'))
print(check_if_username_handler_exists_on_blogspot('alitakos90'))
#'Blog nicht gefunden.' or 'Blog not found' 
#"Blog wurde entfernt.' or 'Blog has been removed'
###require the english form...works