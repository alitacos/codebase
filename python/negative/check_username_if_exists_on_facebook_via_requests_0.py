def check_username_if_exists_on_facebook_via_requests(username:str=''):
    from bs4 import BeautifulSoup
    import requests
    if not username or not isinstance(username, str) or not str(username).strip():
        return  {'error':'invalid username','username':username, 'fullName':None, 'available':False ,'exists':False} 
    try:
        r = requests.get(f"https://www.facebook.com/{str(username).strip().replace(' ','.')}", allow_redirects=True)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text,'html.parser')
            if r.url.replace('https://www.facebook.com/','') == str(username).strip():
                return {'error':False, 'username': r.url.replace('https://www.facebook.com/',''), 'fullName':soup.title.text,'available':False,,'exists':True}
            if r.url.replace('https://www.facebook.com/','') != str(username).strip():
                return {'error':'case_sensitive unmatch redirect', 'username': r.url.replace('https://www.facebook.com/',''), 'fullName':soup.title.text,'available':False,,'exists':True}              
            return {'error':False,'username':username, 'fullName':None, 'available':True, 'exists':False}
        return {'error':r.status_code,'username':username, 'fullName':None, 'available':None, 'exists':None}
    except Exception as e:
        return  {'error':e,'username':username, 'fullName':None, 'available':None ,'exists':None}

#check_username_if_exists_on_facebook_via_requests(username='anonymous@gmail.com')