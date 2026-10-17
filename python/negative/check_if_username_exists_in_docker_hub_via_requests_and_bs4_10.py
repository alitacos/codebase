def check_if_username_exists_in_docker_hub_via_requests_and_bs4(username: str='',retries:int=3, delay: int = 2,url:str=f"https://hub.docker.com/u/" , cookies:dict={}, headers:dict={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}, allow_redirects:bool=False)->dict:
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False}
    for _ in range(retries):
        try:
            response = requests.get( f'{url.strip().rstrip('/')}/{str(username).strip().strip('/')}/', headers=headers, cookies=cookies,allow_redirects=allow_redirects)
            soup = BeautifulSoup(response.text, 'html.parser')
            if response.status_code == 200:
                content = soup.find('div',{'data-testid':'profile-header'})  
                return { 'error':False,"status": 200,"username": username, "content": '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if content else None , "title": soup.title.get_text().strip()   if soup and soup.title else None,"available":False,"exists":True}
            if response.status_code == 404:
                content = soup.find('img',{'data-testid':'404page'}) or soup.find('div',{'data-testid':'profile-header'}) or soup.get_text(strip=True)
                return { 'error':False, "status": 404,"username": username, "content": '\n'.join([i for i in content.get_text().replace('\t','\n').strip().split('\n') if i and i.strip()]) if content else None , "title": soup.title.get_text().strip() if soup and soup.title else None,"available":True,"exists":False}
            # --- unexpected status → retry instead of returning ---
            last_error = f"unexpected status_code {response.status_code}"
            time.sleep(delay)
            continue

            
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None}
print(check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='alitakos90')) 
print(check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='anon')) 
#negative
