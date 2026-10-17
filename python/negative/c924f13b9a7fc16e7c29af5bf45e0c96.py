def get_topics_by_topic_in_github_topics_via_requests_and_bs4(topic:str='',page_no:int=0,lang:str=None)->list:
    """Extract topics from a page"""
    import requests
    from bs4 import BeautifulSoup
    if not topic or not isinstance(topic,str) or not topic.strip():
        #print('ValueError')
        return []
    page_no = 0 if not page_no or not isinstance(page_no,(str,int)) or (isinstance(page_no,str) and not page_no.strip().isdigit()) else int(page_no)
        
    if not lang or not isinstance(lang,str) or not lang.strip():
        lang = None
    url = f'https://github.com/topics/{topic.strip()}?{f"l={lang.lower().strip()}" if lang and lang.strip() else ""}{"&" if page_no else ""}{f"page={int(page_no)}" if page_no else ""}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    topics = soup.find_all('a', class_='topic-tag topic-tag-link Link f6 mb-2')
    return sorted(set([i.get_text().strip() for i in topics if i and i.get_text()]))
