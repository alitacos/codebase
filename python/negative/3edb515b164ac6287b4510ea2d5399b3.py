def extract_topics(topic:str='',page_no:int=0)->list:
    """Extract topics from a page"""
    if not topic or not isinstance(topic,str) or not topic.strip():
        #print('ValueError')
        return []
    if not page_no or not isinstance(page_no,(str,int)) or (isinstance(page_no,str) and not page_no.strip().isdigit()):
        page_no = 0
    url = f'https://github.com/topics/{topic.strip()}?page={int(page_no)}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    topics = soup.find_all('a', class_='no-underline flex-1 d-flex flex-column')
    return sorted(set([i.strip() for i in topics if i and i.strip()]))
