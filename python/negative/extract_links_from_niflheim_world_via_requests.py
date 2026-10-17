uiids = [2684703 ,2684704,2684624,2684710,2684712]# use these as first uiids to test and extract links...

def extract_links_from_niflheim_world_via_requests(user_id:int=None,pages:range=range(1,11)):
    import re
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urlparse
    
    if user_id and isinstance(user_id,str) and user_id.startswith(('http://','https://')):
        parse_uiid = urlparse(user_id)
        if 'niflheim.world' in parse_uiid.netloc:
            user_id = parse_uiid.path.split('/')[-1]
        else:
            return []
    if user_id and ((isinstance(user_id,str) user_id.isdigit()) or isinstance(user_id, int)):
        url = f'https://niflheim.world/search/{int(user_id) if isinstance(user_id,str) else user_id}'
    else:
        return []
    URL_RE = re.compile(r'https?://[^\s<>"\']+', re.IGNORECASE)
    hrefs = set()
    links = set(hrefs)
    for page_no in pages:
        params = {'page':page_no}
        response = requests.get(url,params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        elements = set(soup.find_all(True))
        anchors = set(soup.find_all("a"))
        for element in anchors:
            if element.has_attr("href"):
                hrefs.add(element["href"])
        for element in elements:
            text = element.get_text()
            for link in URL_RE.findall(text):
                links.add(link)
    return links