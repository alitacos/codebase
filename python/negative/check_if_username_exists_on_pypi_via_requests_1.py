def check_if_username_exists_on_pypi_via_requests(username: str='')->dict:
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(f"https://pypi.org/user/{str(username).strip()}/", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"})
    if response.status_code == 200:
        return {"status": 200,"message": "User exists."}
    elif response.status_code == 404:
        return {"status": 404,"message": "User does not exist."}
    
    return {"status": "unknown","message": f"Unexpected status: {response.status_code}"}

# Example usage
#result = check_if_username_exists_on_pypi_via_requests(username='anonymous')
