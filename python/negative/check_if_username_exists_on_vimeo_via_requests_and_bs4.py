def check_if_username_exists_on_vimeo_via_requests(username: str='')->dict:
    import requests
    from bs4 import BeautifulSoup
    try:
        if not username or not isinstance(username, str) or not str(username).strip():
            return {'error':'invalid <username> value', "status": None,"username": username,"content": None}
        username = str(username).strip()
        response = requests.get(f"https://vimeo.com/{username}", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return {"error":False,"status": 200,"username": username,"content": soup.get_text(separator="\n", strip=True)}
        elif response.status_code == 404:
            return {"error":False, "status": 404,"username": username,"content": "User not found."}
        else:
            return {"error":f"Unexpected status: {response.status_code}","status": response.status_code,"username": username,"content":None }
    except Exception as e:
        return {'error':str(e), "status": None,"username": username,"content": None}
        
#result = check_if_username_exists_on_vimeo_via_requests('anonymous')
