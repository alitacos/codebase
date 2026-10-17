def check_if_username_exists_in_docker_hub_via_requests_and_bs4( username: str = '', retries: int = 3, delay: int = 2, url: str = "https://docker.com", cookies: dict = {}, headers: dict = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "application/json, text/html, */*" }, allow_redirects: bool = False ) -> dict:
    import time
    import requests
    import json
    import re
    # Validation check
    if not username or not isinstance(username, str) or not str(username).strip():
        return { 'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None, "available": False, "exists": False }

    clean_url = str(url).strip().rstrip('/')
    clean_username = str(username).strip().strip('/')
    target_url = f"{clean_url}/{clean_username}/"

    last_error = None

    for attempt in range(retries):
        try:
            response = requests.get( target_url, headers=headers, cookies=cookies, allow_redirects=allow_redirects )

            if response.status_code == 200:
                try:
                    data = response.json()
                    full_name = data.get('full_name', '').strip()
                    company = data.get('company', '').strip()
                    location = data.get('location', '').strip()
                    
                    # Synthesize text content properties exactly matching hydration UI strings
                    parts = [username, "Community User"]
                    if full_name:
                        parts.insert(1, full_name)
                    if company:
                        parts.append(company)
                    if location:
                        parts.append(location)
                        
                    content_text = " ".join(parts)
                except Exception:
                    content_text = f"{username} Community User"

                return { 'error': False, "status": 200, "username": username, "content": content_text, "title": username, "available": False, "exists": True }

            if response.status_code == 404:
                return { 'error': False, "status": 404, "username": username, "content": '', "title": 'Page Not Found', "available": True, "exists": False }

            last_error = f"unexpected status_code {response.status_code}"
            time.sleep(delay)
            continue

        except Exception as e:
            last_error = str(e)
            time.sleep(delay)

    return { 'error': last_error, "status": None, "username": username, "content": None, "title": None, "available": None, "exists": None }


# --- Execution Blocks ---
#if __name__ == "__main__":
#    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4('alitakos90'))
#    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4('anon'))
