def check_if_username_exists_in_slides_com_via_requests_and_bs4(username: str='',retries:int=3, delay: int = 2,url:str='https://slides.com/',headers:dict={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"}, cookies:dict={})->dict:
    import time
    import requests
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False}
    for _ in range(retries):
        try:
            response = requests.get(f"{str(url).strip().strip('/')}/{str(username).strip().strip('/')}", headers=headers,cookies=cookies)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code == 200:
                return { 'error':False,"status": 200,"username": username, "content": '\n'.join([i for i in soup.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None , "title": soup.title.text.strip()   if soup and soup.title  else None,"available":False,"exists":True}
            if response.status_code == 404:
                return { 'error':False, "status": 404,"username": username, "content": '\n'.join([i for i in soup.find('div',{'class':'errors-header'}).get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup and soup.find('div',{'class':'errors-header'}) else None , "title": soup.title.text.strip()  if soup   else None,"available":True,"exists":False}
            return {'error':f'unexpected status_code {response.status_code}',"status": response.status_code,"username": username,"content": '\n'.join([i for i in response.text.replace('\t','\n').strip().split('\n') if i and i.strip()]) if soup else None, "title": soup.title if soup else None,"available":None,"exists":None}
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None}
         
# Example usage
#check_if_username_exists_in_slides_com_via_requests_and_bs4(username='anna')
