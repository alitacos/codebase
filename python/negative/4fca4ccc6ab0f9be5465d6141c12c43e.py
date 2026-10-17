def extract_all_main_topics_in_github_to_csv_file(output: str='') -> None:
    import csv
    import requests
    from bs4 import BeautifulSoup
    TOPICS_URL = 'https://github.com/topics'
    LANGUAGES = ['All','tex', 'scss', 'robotframework', 'kotlin', 'crystal', 'angelscript', 'vba', 'css', 'cuda', 'powershell', 'c%2B%2B', 'swift', 'plsql', 'handlebars', 'classic+asp', 'batchfile', 'haskell', 'shell', 'fortran', 'ocaml', 'jupyter+notebook', 'rich+text+format', 'pug', 'nasal', 'postscript', 'haxe', 'typescript', 'shaderlab', 'dart', 'dockerfile', 'javascript', 'apex', 'lasso', 'actionscript', 'yaml', 'asp.net', 'purebasic', 'sass', 'autohotkey', 'r', 'forth', 'gherkin', 'vue', 'blade', 'makefile', 'erlang', 'perl', 'adblock+filter+list', 'yacc', 'python', 'elixir', 'plpgsql', 'visual+basic+.net', 'hack', 'vim+script', 'm', 'objective-c%2B%2B', 'openedge+abl', 'lua', 'astro', 'mdx', 'xslt', 'rescript', 'coffeescript', 'freemarker', 'verilog', 'openscad', 'php', 'html', 'common+lisp', 'ruby', 'nunjucks', 'less', 'objective-c', 'f%23', 'java', 'nix', 'mcfunction', 'assembly', 'yara', 'twig', 'cirru', 'groovy', 'matlab', 'asl', 'jinja', 'roff', 'ejs', 'c', 'kicad+layout', 'c%23', 'applescript', 'julia', 'rust', 'digital+command+language', 'markdown', 'solidity', 'awk', 'clojure', 'logos', 'dm', 'basic', 'tsql', 'api+blueprint', 'go', 'svelte', 'antlr', 'bitbake', 'coq', 'unrealscript', 'nim', 'gdscript', 'hcl', 'emacs+lisp', 'abap', 'standard+ml', 'processing', 'smarty', 'autoit', 'qml', 'g-code', 'cmake', 'total_repos', 'scala', 'pascal', 'hlsl']

    def extract_topics(page_num):
        """Extract topics from a page"""
        url = f'{TOPICS_URL}?page={page_num}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        topics = soup.find_all('a', class_='no-underline flex-1 d-flex flex-column')
        return topics

    def store_topic_data(topic_data, topic_name, topic_url):
        """Store topic data in the CSV file"""
        with open(output, 'a', newline='') as csvfile:
            fieldnames = ['topic', 'name', 'source', 'description', 'processed'] + LANGUAGES
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow({'topic': topic_url.replace('https://github.com/topics/', ''), 'name': topic_name, 'source': topic_url, 'description': topic_data['description'], 'processed': '0 %', **topic_data['languages']})

    def extract_topic_data(topic_url, topic_id):
        """Extract topic data from a topic page"""
        response = requests.get(topic_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        description_element = soup.find('div', class_='markdown-body')
        if description_element is not None:
            description = description_element.find('p').text.strip()
        else:
            description = ''
        total_repos_element = soup.find('h2', class_='h3 color-fg-muted')
        if total_repos_element is not None:
            total_repos = total_repos_element.text.strip()
            words = total_repos.split(' ')
            for word in words:
                if word.replace(',', '').isdigit():
                    total_repos = int(word.replace(',', ''))
                    break
        else:
            total_repos = 0
        languages = soup.find_all('a', class_='select-menu-item')
        language_list = []
        for language in languages:
            language_name = language.text.strip()
            language_list.append(language_name)
        language_list = [lang for lang in language_list if not lang.startswith(('Most', 'Fewest', 'Recently', 'Least', 'recently updated'))]
        language_list = [lang.replace('\n', ':').replace(' ', '').replace('\t', '') for lang in language_list]
        language_counts = {lang: 0 for lang in LANGUAGES}
        if language_list:
            if ':' in language_list[0]:
                all_repos = language_list[0].split(':')[1]
                language_counts['All'] = int(all_repos.replace(',', ''))
                language_list = language_list[1:]
            else:
                all_repos = language_list[0]
                language_counts['All'] = int(all_repos.replace(',', ''))
                language_list = language_list[1:]
        else:
            all_repos = ''
            language_list = []
        for language in language_list:
            if ':' in language:
                lang_name, count = language.split(':')
                lang_name = lang_name.lower()
                if lang_name in LANGUAGES:
                    language_counts[lang_name] = int(count.replace(',', ''))
        return {'topic': topic_id, 'description': description, 'source': topic_url, 'total_repos': total_repos, 'languages': language_counts}
    'Extract GitHub main topics'
    page_num = 1
    while True:
        topics = extract_topics(page_num)
        if not topics:
            break
        for topic in topics:
            topic_url = topic['href']
            topic_name = topic.find('p', class_='f3 lh-condensed mb-0 mt-1 Link--primary').text.strip()
            topic_url = f"https://github.com/topics/{topic_url.split('/')[-1]}"
            topic_id = topic_url.replace('https://github.com/topics/', '')
            topic_data = extract_topic_data(topic_url, topic_id)
            store_topic_data(topic_data, topic_name, topic_url)
            print(topic_id, topic_data)
        page_num += 1
    return None


extract_all_main_topics_in_github_to_csv_file(output='topics_github_base.csv')