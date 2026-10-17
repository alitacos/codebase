def check_ycombinator_userame_via_requests_and_bs4(username: str = '',retries:int=3, delay: int = 2,url:str='https://news.ycombinator.com/user?id=', headers:dict={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}, cookies:dict={})->dict:
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None,"available":False,"exists":False}
    for _ in range(retries):
        try:

            # Send GET request to the user profile URL
            response = requests.get(f"{url}{str(username).strip()}", headers=headers,cookies=cookies)

            # Check if the response status is 200 (OK)
            if response.status_code == 200:
                # Parse the page content with BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.get_text().strip() if soup else ''
                if "No such user." == content:
                    return {'error': False, "status": 200, "username": username, "content": content, "title": soup.title.text if soup and soup.title else None,"available":True,"exists":False}
                else:
                    return {'error': False, "status": 200, "username": username, "content": content, "title": soup.title.text if soup and soup.title else None,"available":False,"exists":True}
            return {'error': f'unexpected status_code {response.status_code}', "status": response.status_code, "username": username, "content": response.text, "title": None,"available":None,"exists":None}
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None,"available":None,"exists":None}

# Example usage
#result = check_ycombinator_userame_via_requests_and_bs4(username='anonymous')
#print(result)