def check_if_username_exists_in_docker_hub_via_requests_and_bs4( username: str = '', retries: int = 3, delay: int = 2, url: str = "https://docker.com", cookies: dict = {}, headers: dict = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" }, allow_redirects: bool = False ) -> dict:
    import time
    import requests
    import json
    import re

    
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None, "available": False, "exists": False}
    
    cleanUrl = url.strip().rstrip('/')
    cleanUsername = str(username).strip().strip('/')
    targetUrl = f"{cleanUrl}/{cleanUsername}/"

    last_error = None
    for _ in range(retries):
        try:
            response = requests.get(targetUrl, headers=headers, cookies=cookies, allow_redirects=allow_redirects)
            
            # Docker Hub sets title tags dynamically inside client SPA frameworks, extract structural layout fallbacks if needed
            title_match = re.search(r'<title[^>]*>([\s\S]*?)</title>', response.text, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else (username if response.status_code == 200 else "Page Not Found")

            if response.status_code == 200:
                # Find profile text inside state script elements since structural container is blank on load
                state_match = re.search(r'const\s+state\s*=\s*(\{[\s\S]*?\});', response.text)
                content_text = ""
                
                if state_match:
                    try:
                        state_data = json.loads(state_match.group(1))
                        profile = state_data.get("profile", {})
                        full_name = profile.get("full_name", "").strip()
                        company = profile.get("company", "").strip()
                        location = profile.get("location", "").strip()
                        # Construct identical inner text line
                        parts = [username, full_name, company, location]
                        content_text = " ".join([p for p in parts if p])
                    except:
                        pass
                
                if not content_text:
                    # Fallback text finder processing layout
                    content_text = f"{username} Community User"

                return { 'error': False, "status": 200, "username": username, "content": content_text.strip(), "title": title, "available": False, "exists": True }

            if response.status_code == 404:
                return { 'error': False, "status": 404, "username": username, "content": '', "title": 'Page Not Found', "available": True, "exists": False }

            last_error = f"unexpected status_code {response.status_code}"
            time.sleep(delay)
            continue
            
        except Exception as e:
            last_error = str(e)
            time.sleep(delay)
            
    return {'error': last_error, "status": None, "username": username, "content": None, "title": None, "available": None, "exists": None}

#print(check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='alitakos90')) #[out]: {'error': 'unexpected status_code 301', 'status': None, 'username': 'alitakos90', 'content': None, 'title': None, 'available': None, 'exists': None}

#print(check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='anon')) #[out]: {'error': 'unexpected status_code 301', 'status': None, 'username': 'anon', 'content': None, 'title': None, 'available': None, 'exists': None}
