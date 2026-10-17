def check_if_user_handle_exists_in_youtube_via_requests(url: str):
    import requests
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, allow_redirects=False)
    if r.status_code in (301, 302, 303, 307, 308):
        location = r.headers.get("Location", "")
        if "/channel/" in location:
            return {"status": 200, "exists": True, "redirect": location}
        if "/error" in location or "oops" in location:
            return {"status": 404, "exists": False}
    if r.status_code == 404 :
        return {"status": 404, "exists": False}

    # Unexpected cases
    return {"status": r.status_code, "exists": None, "info": r.text[:200]}
#print(youtube_handle_exists("https://www.youtube.com/@anonymous")) # out: {'status': 302, 'exists': None, 'info': ''}
