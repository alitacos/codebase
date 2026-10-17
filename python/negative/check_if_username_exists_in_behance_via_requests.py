 def check_if_username_exists_in_behance_via_requests(url: str):
    import requests
    from bs4 import BeautifulSoup
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"}

    r = requests.get(url, headers=headers)

    # Return only the status if the page is not OK
    if r.status_code != 200:
        try:
            return {"status": r.status_code,"text": r.json()}
        except Exception:
            soup = BeautifulSoup(r.text, "html.parser")
            return {"status": r.status_code,"text": soup.text}
    else:
        soup = BeautifulSoup(r.content, "html.parser")
        return {"status": r.status_code,"text":r.text}#
         
