# need to check title, get info of user if exists, else rerurn that not exists
def check_if_username_exists_on_flickr_via_requests_and_bs4(username: str = '', retries: int = 3, delay: int = 2) -> dict:
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None, "url": None}

    for _ in range(retries):
        try:
            r = requests.get(f"https://www.flickr.com/people/{username}", headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"
            })

            if r.status_code in [200, 404]:
                soup = BeautifulSoup(r.text, "html.parser")
                return {'error': False, "status": r.status_code, "username": username, "content": soup.get_text(separator="\n", strip=True), "title": soup.title, "url": r.url}
            return {'error': 'unexpected status_code', "status": r.status_code, "username": username, "content": r.text, "title": None, "url": r.url}
        except Exception as e:
            time.sleep(delay)  # Wait before retrying
            last_error = str(e)
    
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None, "url": None}

# Test
result = check_if_username_exists_on_flickr_via_requests_and_bs4(username='anonymous')
print(result)
