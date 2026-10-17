def check_if_username_handler_exists_on_twitter(target:str='',allow_redirects:bool=True)->tuple:
    """
    Attempts to check whether a Twitter/X username exists by requesting
    the corresponding profile page and extracting visible text content.

    The function sends an HTTP request to the profile URL and parses the
    returned HTML using BeautifulSoup. Since the platform heavily relies
    on JavaScript, the response may not contain meaningful profile data,
    and instead return a fallback message if JavaScript is required.

    Args:
        target (str): The Twitter/X username (without '@') to check. (Defaults to '')
        allow_redirects (bool): Whether to follow HTTP redirects during the request. (Defaults to True)

    Returns:
        tuple: A tuple containing:
            - str: Extracted visible text from the HTML response
            - str: Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_twitter(target='username', allow_redirects=True)
    """
    from bs4 import BeautifulSoup
    import requests
    #header = {"content-type": "application/x-www-form-urlencoded; charset=UTF-8","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",              "x-requested-with": "XMLHttpRequest"}
    r = requests.post(f"https://x.com/{target}",  headers=None, cookies=None, allow_redirects=allow_redirects)

    return BeautifulSoup(r.text,'html.parser').get_text().strip(),r.url
#print(check_if_username_handler_exists_on_twitter('anonymous'))##('JavaScript is not available.\nWe’ve detected that JavaScript is disabled in this browser. Please enable JavaScript or switch to a supported browser to continue using x.com. You can see a list of supported browsers in our Help Center.\nHelp Center\n\nTerms of Service\nPrivacy Policy\nCookie Policy\nImprint\nAds info\n      © 2026 X Corp.\n    \nSomething went wrong, but don’t fret — let’s give it another shot.Try again Some privacy related extensions may cause issues on x.com. Please disable them and try again.', 'https://x.com/anonymous')
###NOT WORKING...REQUIRES TO ENABLE JAVASCRIPT