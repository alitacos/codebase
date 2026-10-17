def check_username_if_exists_on_facebook_via_requests(username:str=''):
    from bs4 import BeautifulSoup
    import requests
    try:
        r = requests.get(f"https://www.facebook.com/{str(username).strip().replace(' ','.')}", allow_redirects=True)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text,'html.parser')
            return {'error':False, 'username': r.url.replace('https://www.facebook.com/',''), 'Name':soup.title.text,}
        return {'error':r.status_code,'username':None, 'Name':None, }
    except Exception as e:
        return  {'error':e,'username':None, 'Name':None,  }