def check_if_username_exists_in_docker_hub_via_requests_and_bs4( username: str = '', retries: int = 3, delay: int = 2, url: str = "https://hub.docker.com/u/", cookies: dict = {}, headers: dict = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8" }, allow_redirects: bool = False ) -> dict:
    import time
    import requests
    import re

    # 1:1 Translation of string validation check
    if not username or not isinstance(username, str) or not str(username).strip():
        return { 'error': 'invalid <username> value', "status": None, "username": username, "content": None, "title": None, "available": False, "exists": False }

    # Handle cookies passing mechanics directly via requests engine parameters mapping
    request_cookies = cookies

    # Exact string combination mechanics replication
    clean_url = str(url).strip().rstrip('/')
    clean_username = str(username).strip().strip('/')
    target_url = f"{clean_url}/{clean_username}/"

    # 1:1 Replica of: bs4GetTextComprehension
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
            # Replicating manual fetch mechanics using requests configurations
            response = requests.get( target_url, headers=headers, cookies=request_cookies, allow_redirects=False )

            # Manual redirection handler simulation block
            if response.status_code in:
                if allow_redirects:
                    location = response.headers.get('location')
                    if location:
                        target_url = location
                        response = requests.get(target_url, headers=headers, cookies=request_cookies, allow_redirects=False)

            html_text = response.text

            # Replicating JS title regex capture index [1] logic explicitly
            title_match = re.search(r'<title[^>]*>([\s\S]*?)</title>', html_text, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else (username if response.status_code == 200 else "Page Not Found")

            if response.status_code == 200:
                content_text = ""
                profile_header_match = re.search(r'<div[^>]*data-testid=["\']profile-header["\'][^>]*>([\s\S]*?)</div>', html_text, re.IGNORECASE)
                
                if profile_header_match and profile_header_match.group(1):
                    content_text = bs4_get_text_comprehension(profile_header_match.group(1))
                
                if not content_text or content_text.strip() == "":
                    content_text = f"{username} Community User"

                return { 'error': False, "status": 200, "username": username, "content": content_text, "title": title, "available": False, "exists": True }

            if response.status_code == 404:
                content_text = None
                error_page_match = re.search(r'<img[^>]*data-testid=["\']404page["\'][^>]*>([\s\S]*?)(?:/>|</img>)', html_text, re.IGNORECASE)
                
                if error_page_match and error_page_match.group(1):
                    content_text = bs4_get_text_comprehension(error_page_match.group(1))

                return { 'error': False, "status": 404, "username": username, "content": content_text if content_text is not None else "", "title": title, "available": True, "exists": False }

            last_error = f"unexpected status_code {response.status_code}"
            time.sleep(delay)
            continue

        except Exception as e:
            last_error = str(e)
            time.sleep(delay)

    return { 'error': last_error, "status": None, "username": username, "content": None, "title": None, "available": None, "exists": None }


# --- Execution Execution Pipeline Validation Logs ---
#if __name__ == "__main__":
#    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4('alitakos90'))
#    print(check_if_username_exists_in_docker_hub_via_requests_and_bs4('anon'))
