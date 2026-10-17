import time
import requests
import re
from bs4 import BeautifulSoup

def check_if_username_exists_in_docker_hub_via_requests_and_bs4(
    username: str = '',
    retries: int = 3,
    delay: int = 2,
    url: str = "https://docker.com",
    cookies: dict = {},
    headers: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    },
    allow_redirects: bool = False
) -> dict:
    
    # Complete type and layout validation check
    if not username or not isinstance(username, str) or not str(username).strip():
        return { 'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None, "available": False, "exists": False }

    clean_url = str(url).strip().rstrip('/')
    clean_username = str(username).strip().strip('/')
    target_url = f"{clean_url}/{clean_username}/"

    def bs4_get_text_comprehension(html_block):
        if not html_block:
            return ""
        # Strip internal tags via regular expression replacements to simulate standard innerText extractions
        stripped = re.sub(r'<[^>]*>', ' ', html_block)
        lines = stripped.replace('\t', '\n').strip().split('\n')
        processed_lines = [i.strip() for i in lines if i and i.strip() != '']
        return '\n'.join(processed_lines)

    last_error = None

    for attempt in range(retries):
        try:
            # We fetch manually first to emulate JavaScript custom redirection control
            response = requests.get(
                target_url, 
                headers=headers, 
                cookies=cookies, 
                allow_redirects=False
            )

            # Correctly handle 3xx status codes to follow redirects when allow_redirects=True, 
            # or treat them as a continuous retry error when allow_redirects=False.
            if response.status_code in [301, 302, 303, 307, 308]:
                if allow_redirects:
                    location = response.headers.get('location')
                    if location:
                        target_url = location
                        response = requests.get(target_url, headers=headers, cookies=cookies, allow_redirects=False)
                else:
                    last_error = f"unexpected status_code {response.status_code}"
                    time.sleep(delay)
                    continue

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
                # Target the 404 image tag or fallback error layouts explicitly
                content = soup.find('img', {'data-testid': '404page'}) or soup.find('div', {'data-testid': 'profile-header'})
                
                if content and content.get_text(strip=True):
                    content_text = '\n'.join([i for i in content.get_text().replace('\t', '\n').strip().split('\n') if i and i.strip()])
                else:
                    content_text = ""

                return {
                    'error': False,
                    "status": 404,
                    "username": username,
                    "content": content_text,
                    "title": title,
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
#if __name__ == "__main__":
    # Setting allow_redirects=True makes sure 301 redirects to the actual profiles are followed cleanly
#    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='alitakos90', allow_redirects=True))
#    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4(username='anon', allow_redirects=True))
