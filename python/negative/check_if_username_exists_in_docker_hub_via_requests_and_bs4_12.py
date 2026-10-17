    
def check_if_username_exists_in_docker_hub_via_requests_and_bs4( username: str = '', retries: int = 3, delay: int = 2, url: str = "https://hub.docker.com/u/", cookies: dict = {}, headers: dict = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" }, allow_redirects: bool = False ) -> dict:    
    import time
    import requests
    import re
    from bs4 import BeautifulSoup

    # Complete type and layout validation check
    if not username or not isinstance(username, str) or not str(username).strip():
        return { 'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None, "available": False, "exists": False }

    clean_url = str(url).strip().rstrip('/')
    clean_username = str(username).strip().strip('/')
    target_url = f"{clean_url}/{clean_username}/"

    last_error = None

    for attempt in range(retries):
        try:
            # We explicitly catch redirects first if allow_redirects is configured
            response = requests.get(
                target_url, 
                headers=headers, 
                cookies=cookies, 
                allow_redirects=allow_redirects
            )

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Safe title extraction matching uniform layout behaviors
            title = soup.title.get_text().strip() if soup and soup.title else (username if response.status_code == 200 else "Page Not Found")

            if response.status_code == 200:
                content = soup.find('div', {'data-testid': 'profile-header'})
                
                # Check if layout contains hydrated texts or build exact structural fallbacks
                if content and content.get_text(strip=True):
                    content_text = '\n'.join([i for i in content.get_text().replace('\t', '\n').strip().split('\n') if i and i.strip()])
                else:
                    content_text = f"{username} Community User"

                return {
                    'error': False,
                    "status": 200,
                    "username": username,
                    "content": content_text,
                    "title": title,
                    "available": False,
                    "exists": True
                }

            if response.status_code == 404:
                # Docker Hub returns empty text over server-side render shells for 404 failures
                return {
                    'error': False,
                    "status": 404,
                    "username": username,
                    "content": '',
                    "title": 'Page Not Found',
                    "available": True,
                    "exists": False
                }

            last_error = f"unexpected status_code {response.status_code}"
            time.sleep(delay)
            continue

        except Exception as e:
            last_error = str(e)
            time.sleep(delay)

    return { 'error': last_error, "status": None, "username": username, "content": None, "title": None, "available": None, "exists": None }


# --- Execution Blocks ---
if __name__ == "__main__":
    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4('alitakos90'))
    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4('anon'))
