def check_if_username_exists_on_flickr_via_requests_and_bs4(username:str='')->dict:
    import requests
    from bs4 import BeautifulSoup
    if not username or not isinstance(username, str) or not str(username).strip():
        return {'error':'invalid <username> value', "status": None,"username": username,"content": None, "title":None,"url":None}
    try:
        r = requests.get(f"https://www.flickr.com/people/{username}", headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9, image/avif,image/webp,*/*;q=0.8"})
        
        if r.status_code in [ 200,404]:    
            soup = BeautifulSoup(r.text, "html.parser")
            return {'error':False,"status": r.status_code,"username": username,"content": soup.get_text(separator="\n", strip=True), "title":soup.title,"url":r.url}
        return {'error':'unexpected status_code',"status": r.status_code,"username": username,"content": r.text, "title":None,"url":r.url}
    except Exception as e:
        return {'error':str(e), "status": None,"username": username,"content": None, "title":None,"url":None}
#check_if_username_exists_on_flickr_via_requests_and_bs4(username='anonymous')
