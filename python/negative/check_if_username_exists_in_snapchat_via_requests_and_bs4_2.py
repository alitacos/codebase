
def check_if_username_exists_in_snapchat_via_requests_and_bs4(username: str='')->dict:
    import requests
    from bs4 import BeautifulSoup
    url = f'"https://www.snapchat.com/@{str(username).strip().lstrip('@')}'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return {"status": 200,"url": url,"soup_text": soup.get_text(separator="\n", strip=True)}
    elif response.status_code == 404:
        return {"status": 404,"url": url,"soup_text": "User not found."}
    else:
        return {"status": response.status_code,"url": url,"soup_text": f"Unexpected status: {response.status_code}"}

# Example usage
#print(check_if_username_exists_in_snapchat_via_requests_and_bs4('anonymous')) 
#print(check_if_username_exists_in_snapchat_via_requests_and_bs4('anonksiksuudihbuzdzzuivzvizvzi'))