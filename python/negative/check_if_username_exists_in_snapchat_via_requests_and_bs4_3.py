#error
def check_if_username_exists_in_snapchat_via_requests_and_bs4(username: str='',retries:int=3, delay: int = 2,url:str='https://www.behance.net/',headers:dict={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"},cookies:dict={})->dict:
    import time
    import requests
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False}
    for _ in range(retries):
        try:
            response = requests.get(f"{str(url).strip().strip('/')}/{str(username).strip()}", headers=headers, cookies=cookies)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div',{'id':'site-content'}) if soup else None
            if response.status_code == 200:
                return { 'error':False,"status": 200,"username": username, "content": '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if content else None , "title": soup.title.get_text().strip() if soup and soup.title else None,"available":False,"exists":True}
            if response.status_code == 404:
                return { 'error':False, "status": 404,"username": username, "content": '\n'.join([i for i in content.find('div',{'class':'errors-header'}).get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if content and content.find('div',{'class':'errors-header'}) else None , "title": soup.title.get_text().strip() if soup and soup.title else None,"available":True,"exists":False}
            last_error = f'unexpected status_code {response.status_code}'
            time.sleep(delay)
            continue
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None}
         
# Example usage
#print(check_if_username_exists_in_snapchat_via_requests_and_bs4('anonymous'))
#print(check_if_username_exists_in_snapchat_via_requests_and_bs4('alexpapatolios90'))
#error, missing bs4