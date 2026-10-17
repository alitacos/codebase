def extract_topic_description_of_github_topic_via_requests_and_bs4(topic_id: str='') -> str:
    """
	    [MASKED]

    Args:
        topic_id (str): [MASKED] (Defaults to '')

    Returns:
        str: [MASKED]

    Example usage:
        >>> result = extract_topic_description_of_github_topic_via_requests_and_bs4(topic_id='[MASKED]')
    	"""
    import requests
    from bs4 import BeautifulSoup
    'Extract topic´s description text from a topic page'
    topic_url = 'https://github.com/topics/' + topic_id
    try:
        response = requests.get(topic_url + f'?page=1')
        soup = BeautifulSoup(response.content, 'html.parser')
        description_element = soup.find('div', class_='markdown-body') if soup else None
        description = description_element.find('p').text.strip()
        return description
    except Exception as e2:
        return None