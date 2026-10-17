def extract_topic_description_html_element_of_github_topic(topic_id: str='') -> str:
    import requests
    from bs4 import BeautifulSoup
    'Extract topic´s description text from a topic page'
    topic_url = 'https://github.com/topics/' + topic_id
    try:
        response = requests.get(topic_url + f'?page=1')
        soup = BeautifulSoup(response.content, 'html.parser')
        description_element = soup.find('div', class_='markdown-body') if soup else None
        return description_element
    except Exception as e2:
        return None