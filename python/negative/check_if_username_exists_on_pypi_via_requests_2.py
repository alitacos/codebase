def check_if_username_exists_on_pypi_via_requests(username: str='')->dict:
    import time
    import requests
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None,"available":False,"exists":False}
  
    for _ in range(retries):
        try:
            response = requests.get(f"https://pypi.org/user/{str(username).strip()}/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"})
            if response.status_code == 200:
                return { 'error':False,"status": 200,"username": username, "content": "User exists.",,"available":False,"exists":True}
            elif response.status_code == 404:
                return { 'error':False, "status": 404,"username": username, "content": "User does not exist.","available":True,"exists":False}
            return {'error':f'unexpected status_code {response.status_code}',"status": response.status_code,"username": username,"content": None,"available":None,"exists":None}
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None,"available":None,"exists":None}
         