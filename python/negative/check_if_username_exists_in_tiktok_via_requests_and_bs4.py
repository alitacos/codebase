def check_if_username_exists_in_tiktok_via_requests_and_bs4(username: str='',retries:int=3, delay: int = 2)->dict:
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False,"isDeleted":None}
    for _ in range(retries):
        try:
            response = requests.get(f"https://www.tiktok.com/@{str(username).strip().lstrip('@')}", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"})
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div',{'data-e2e':'user-page'}) # no matter
            if response.status_code == 200:
                # if 200 the first step is done, else returns error
                # if 200 next check the content to deside if exists, if available or if deleted
                ## problem: soup has always same content...i assume it loads dynamically
                # test 1 without <content> does not work
                #return { 'error':False,"status": response.status_code,"username": username, "content": '\n'.join([i for i in soup.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None , "title": soup.title.get_text()   if soup and soup.title else None,"available":None,"exists":None,"isDeleted":None}
                # test 2 with <content> does not work
                ## why do i get no content???? why do i get no title??? on browser i see the html loading and no js, nothing else 
                return { 'error':False,"status": response.status_code,"username": username, "content": '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup and content else None , "title": soup.title.get_text()   if soup and soup.title else None,"available":None,"exists":None,"isDeleted":None}
            return {'error':f'unexpected status_code {response.status_code}',"status": response.status_code,"username": username,"content": '\n'.join([i for i in response.text.replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None, "title": soup.title if soup else None,"available":None,"exists":None,"isDeleted":None}

        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None,"isDeleted":None}
#print(check_if_username_exists_in_tiktok_via_requests_and_bs4(username='anonymous'))#out:{'error': False, 'status': 200, 'username': 'anonymous', 'content': None, 'title': 'TikTok - Make Your Day', 'available': None, 'exists': None, 'isDeleted': None}
