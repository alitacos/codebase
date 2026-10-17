# does not return in dict if username is available and if username really exists
def check_if_username_exists_on_vimeo_via_requests(username: str = '', retries: int = 3, delay: int = 2) -> dict:
    import time
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None}
    
    username = str(username).strip()
    
    for _ in range(retries):
        try:
            response = requests.get(f"https://vimeo.com/{username}", headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
            })
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                return {"error": False, "status": 200, "username": username, "content": soup.get_text(separator="\n", strip=True)}
            elif response.status_code == 404:
                return {"error": False, "status": 404, "username": username, "content": "User not found."}
            else:
                return {"error": f"Unexpected status: {response.status_code}", "status": response.status_code, "username": username, "content": None}
        
        except Exception as e:
            time.sleep(delay)  # Wait before retrying
            last_error = str(e)
    
    return {'error': last_error, "status": None, "username": username, "content": None}

# Test
result = check_if_username_exists_on_vimeo_via_requests('anonymous')
print(result)
