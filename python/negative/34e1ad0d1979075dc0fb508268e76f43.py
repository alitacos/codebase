def collect_default_github_topics_dict_of_github_topics_page(url_base_topics: str='https://github.com/topics', topic_pages: range=range(1, 7)) -> list:
    topics = []
    for page_num in topic_pages:
        url = f'{url_base_topics}?page={page_num}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.find_all('a', class_='no-underline flex-1 d-flex flex-column')
            for element in elements:
                topic_href = element['href']
                topic_name = element.find('p', class_='f3 lh-condensed mb-0 mt-1 Link--primary').text.strip()
                topic_url = f"https://github.com/topics/{topic_href.split('/')[-1]}"
                topic_id = topic_url.replace('https://github.com/topics/', '')
                topic = {'name': topic_name, 'url': topic_url, 'id': topic_href.split('/')[-1]}
                topics.append(topic)
        else:
            pass
    return topics