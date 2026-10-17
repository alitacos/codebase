def check_if_username_exists_in_reddit_via_requests_and_bs4(username: str='')->dict:
    import requests
    from bs4 import BeautifulSoup
    url = f"https://www.reddit.com/user/{username}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",}
    resp = requests.get(url, headers=headers)
    #resp.raise_for_status()  # will throw if status != 200
    # parse with BeautifulSoup
    soup = BeautifulSoup(resp.content, "html.parser")
    print(resp.status_code)
    return soup

#example usage:
#fetch_reddit_user_page_via_requests_and_bs4(username='anna')