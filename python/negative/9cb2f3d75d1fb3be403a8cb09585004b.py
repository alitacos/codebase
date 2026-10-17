def check_if_username_handler_exists_on_xbox(target: str = '', allow_redirects: bool = True) -> dict:
    """
    Check if an Xbox username exists using the PlayerDB API.

    Args:
        target (str): The Xbox username to check, e.g., 'testuser'.
        allow_redirects (bool): Whether HTTP redirects should be followed. Defaults to True.

    Returns:
        dict: A dictionary containing:
            - title (str | None): The <title> of the response page, if present.
            - status_code (int): The HTTP status code of the response (200 if exists, 404 if not).
            - raw (str): The response text with whitespace cleaned.
            - redirect (str): The final URL after any redirects.

    Notes:
        - Status code 200 generally indicates the username exists.
        - Status code 404 generally indicates the username does not exist.
        - The 'raw' field can be used for debugging or logging the response content.

    Example usage:
        >>> check_if_username_handler_exists_on_xbox('testuser')
        {
            'title': 'PlayerDB API Response',
            'status_code': 200,
            'raw': '{"success":true,"player":{"id":"...","username":"testuser"}}',
            'redirect': 'https://playerdb.co/api/player/xbox/testuser'
        }

        >>> check_if_username_handler_exists_on_xbox('nonexistentuser123')
        {
            'title': None,
            'status_code': 404,
            'raw': '{"success":false,"player":null}',
            'redirect': 'https://playerdb.co/api/player/xbox/nonexistentuser123'
        }
    """
    import requests
    from bs4 import BeautifulSoup
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    url=f"https://playerdb.co/api/player/xbox/{target}"
    r = requests.get(f"{url}", headers=headers, cookies=None, allow_redirects=allow_redirects)
    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]),'redirect':r.url}
##works via status code
#print(check_if_username_handler_exists_on_xbox('test'))# {'title': "Test's Pastebin - Pastebin.com", 'status_code': 200, 'raw': "Test's Pastebin - Pastebin.comPastebinAPItoolsfaqpasteLoginSign upTest's Pastebinhttps://ethercalc.org/3m23o5a9wt33,9241,279014 years agoName / TitleAddedExpiresHitsCommentsSyntaxpw[]pastecarradeNov 15th, 2017Never6220Kotlin-pastebin faqFeb 16th, 2014Never2700HTML-BUCH AUF REISENDec 31st, 2013Never1890None-fehlerDec 15th, 2012Never1980Ruby-Public PastesUntitled2 min ago| 6.10 KBclearTunic26 min ago| 0.26 KBenviroment26 min ago| 0.34 KBvariables40 min ago| 1.81 KBUntitled3 hours ago| 10.43 KBUntitled5 hours ago| 13.45 KBUntitled9 hours ago| 8.95 KBUntitled11 hours ago| 6.86 KBcreate new paste \xa0/syntax languages \xa0/archive \xa0/faq \xa0/tools \xa0/night mode \xa0/api \xa0/scraping api \xa0/news \xa0/proprivacy statement \xa0/cookies policy \xa0/terms of service\xa0/security disclosure \xa0/dmca \xa0/report abuse \xa0/contactBy using Pastebin.com you agree to our cookies policy to enhance your experience.Site design & logo © 2026 PastebinWe use cookies for various purposes including analytics. By continuing to use Pastebin, you agree to our use of cookies as described in the Cookies Policy.            \xa0OK, I UnderstandNot a member of Pastebin yet?Sign Up, it unlocks many cool features!", 'redirect': 'https://pastebin.com/u/test'}
#print(check_if_username_handler_exists_on_xbox('alitajsksdbdsibhhsduwjnwnnwnwjk'))# {'title': 'Pastebin.com - Not Found (#404)', 'status_code': 404, 'raw': 'Pastebin.com - Not Found (#404)PastebinAPItoolsfaqpasteLoginSign upNot Found (#404)The requested page does not exist.Public PastesclearTunic22 min ago| 0.26 KBenviroment22 min ago| 0.34 KBvariables36 min ago| 1.81 KBUntitled2 hours ago| 10.43 KBUntitled4 hours ago| 13.45 KBUntitled8 hours ago| 8.95 KBUntitled10 hours ago| 6.86 KBUntitled12 hours ago| 8.08 KBcreate new paste \xa0/syntax languages \xa0/archive \xa0/faq \xa0/tools \xa0/night mode \xa0/api \xa0/scraping api \xa0/news \xa0/proprivacy statement \xa0/cookies policy \xa0/terms of service\xa0/security disclosure \xa0/dmca \xa0/report abuse \xa0/contactBy using Pastebin.com you agree to our cookies policy to enhance your experience.Site design & logo © 2026 PastebinWe use cookies for various purposes including analytics. By continuing to use Pastebin, you agree to our use of cookies as described in the Cookies Policy.            \xa0OK, I UnderstandNot a member of Pastebin yet?Sign Up, it unlocks many cool features!', 'redirect': 'https://pastebin.com/u/alitajsksdbdsibhhsduwjnwnnwnwjk'}
#works