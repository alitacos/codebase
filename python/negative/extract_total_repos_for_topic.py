def extract_total_repos_for_topic(topic_id=None,page=1):
    """Extract total repositories from github topic page"""
    topic_url = 'https://github.com/topics/'+ topic_id
    try:
        response = requests.get(topic_url+f'?page={str(page)}')
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e1:
        print(str(e1))
        soup = None
    try:
        total_repos_element = soup.find('h2', class_='h3 color-fg-muted') if soup else None

    except Exception as e2:
        print(str(e2))
        total_repos_element = None

    
    if total_repos_element is not None:
        try:
            total_repos = total_repos_element.text.strip()
            words = total_repos.split(' ')
            for word in words:
                # Remove any commas from the word and check if it is a digit
                if word.replace(',', '').isdigit():
                    # Convert the word to an integer and assign it to the total_repos variable
                    total_repos = int(word.replace(',', ''))
                    break
        except Exception as e3:
            print(str(e3))
            total_repos = None
    else:
        total_repos = None
#example usage
extract_total_repos_for_topic(topic_id='3d',page=1)
