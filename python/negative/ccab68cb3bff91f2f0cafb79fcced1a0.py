def check_if_username_handler_exists_on_keybase(target:str='',allow_redirects:bool=True )->tuple:
    """
    Performs an HTTP GET request to a Keybase user page constructed from the
    given username and returns parsed information from the response.

    The input string is directly inserted into the URL "https://keybase.io/<target>"
    without validation. The function does not guarantee that the username exists;
    it only retrieves the page content and metadata.

    Args:
        target (str): Username to insert into the Keybase URL. (Defaults to '')
        allow_redirects (bool): Whether the request should follow HTTP redirects. (Defaults to True)

    Returns:
        dict: A dictionary containing:
            - title (str | None): Content of the <title> tag if present
            - status_code (int): HTTP response status code
            - raw (str): Cleaned visible text extracted from the HTML response
            - redirect (str): Final URL after any redirects

    Example usage:
        >>> result = check_if_username_handler_exists_on_keybase(
        ...     target='example',
        ...     allow_redirects=True
        ... )
    """
    import requests
    from bs4 import BeautifulSoup
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    url=f"https://keybase.io/{target}"
    r = requests.get(f"{url}", headers=headers, cookies=None, allow_redirects=allow_redirects)
    return {'title':BeautifulSoup(r.text,'html.parser').find('title').get_text() if BeautifulSoup(r.text,'html.parser').find('title') else None,'status_code':r.status_code,'raw':''.join([i.strip() for i in BeautifulSoup(r.text,'html.parser').get_text().strip().split('\n') if i and i.strip()]),'redirect':r.url}
##works via status code
#print(check_if_username_handler_exists_on_keybase('test'))# {'title': "test ('my' test account) | Keybase", 'status_code': 200, 'raw': "test ('my' test account) | KeybaseKeybase Staging ServerInstallLogin××test'my' test accountChat with testStart a chatYour conversation will be end-to-end encrypted.45141DF80DA48748Chat with testStart a chatYour conversation will be end-to-end encrypted.Following (0)Followers (34)kwonjencultavixJames Eaton GonzaleznoiselabsVítor BrandãoyoviwankenobiOvi BorrerochansenzsoltnemethMira BarnakakannyumezhHvostenko Akulinaalwine72Eva RuppfermoselleAngel Fermoselle EsclapebigtonygreniaLoad 24 moreBrowse others (14)troyTroy GoodeajungeAndrés Junge Mac-EvoyhoodossHoodosslainadDanialsw1nnkisbitcoinKEEP IT SIMPLE BITCOINwangpronhallNatecrgosselinChris Gosselinceek_seekkimhardingjilliechapel2rJillie Chapelaliciagreyfordfusion76What the heck is Keybase?Keybase is an open source appKeybase comes with everything you need to manage your identity,create secure chats, and share files privately. It's free.It's fun too.Over 100,000 people have joined Keybase so far to prove their identities, and it's growing rapidly.Keybase, 2026| Available within Tor at http://keybase5wmilwokqirssclfnsqrjdsi7jdir5wy7y7iu3tanwmtp6oid.onioninstall Keybase| read our blog| documentation| bug reporting| security advisoriesterms& privacy& california ccpa& acceptable usejobs @ keybasePlease send us feedback & bug reports.Keybase, 2026| read our blogterms& privacy& security advisories& california ccpa& acceptable use", 'redirect': 'https://keybase.io/test'}
#print(check_if_username_handler_exists_on_keybase('alitajsksdbdsibhhsduwjnwnnwnwjk'))# {'title': None, 'status_code': 404, 'raw': '404 - sorry, not found.', 'redirect': 'https://keybase.io/alitajsksdbdsibhhsduwjnwnnwnwjk'}
#works