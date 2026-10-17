def check_if_youtube_handle_exists_via_requests_and_bs4(handle: str):
    import requests
    try:
        r = requests.get(f"https://www.youtube.com/@{handle}/featured", headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.content, 'html.parser')
        # the requests method does not work even if improved... but if would work following lines would required modification
        return {"error":False, "exists": None, "status": r.status_code, "debug": soup.get_text() }
    except Exception as e:
        return {"error":str(e), "exists": None, "status": r.status_code, "debug": soup.get_text() }
        
#print(youtube_handle_exists("anonymous"))
