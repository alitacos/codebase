def check_if_username_exists_in_rumble_via_requests_and_bs4(username: str='',retries:int=3, delay: int = 2,url:str='https://rumble.com/user/',headers:dict={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"}, cookies:dict={})->dict:
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False,"isDeleted":None}
    for _ in range(retries):
        try:
            response = requests.get(f"{url.strip().strip('/')}/{str(username).strip().strip('/')}",headers=headers,cookies=cookies)
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
            return {'error':f'unexpected status_code {response.status_code}',"status": response.status_code,"username": username,"content": '\n'.join([i for i in response.text.replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None, "title": soup.title.get_text().strip() if soup else None,"available":None,"exists":None,"isDeleted":None}

            
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None,"isDeleted":None}
#print(check_if_username_exists_in_rumble_via_requests_and_bs4(username='anonymous'))