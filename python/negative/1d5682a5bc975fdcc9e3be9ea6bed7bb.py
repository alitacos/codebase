#MISSING parsing of topic_id. now for c++ we need to pass  'c%2B%2B' or c# would be 'c%23'. we need to parse it via urllib in code and fix it
def get_metadata_of_topic_in_github_via_requests_and_bs4(topic_id:str='',lang:str=None,page_no:int=0, retries:int=1,delay:int=2,timeout:int=3, **kwargs):
    import requests  # Importing the requests library to handle HTTP requests
    from bs4 import BeautifulSoup  # Importing BeautifulSoup to parse the HTML content of the response
    import time

    if not topic_id or not isinstance(topic_id, str) or not topic_id.strip():  # Check if the topic is a valid non-empty string
        return []  # Return an empty list if the topic_id is invalid
    if not lang or not isinstance(lang, str) or not lang.strip():  # Check if language is a valid non-empty string
        lang = None  # If not valid, set lang to None (no language filter)
    description, total_repos, language_counts ,url,status_code,topic_name=None,  None, None, None,None,None
    LANGUAGES = ['abap', 'actionscript', 'adblock+filter+list', 'all', 'angelscript', 'antlr', 'apex', 'api+blueprint', 'applescript', 'asl', 'asp.net', 'assembly', 'astro', 'autohotkey', 'autoit', 'awk', 'basic', 'batchfile', 'bitbake', 'blade', 'c', 'c%23', 'c%2B%2B', 'cirru', 'classic+asp', 'clojure', 'cmake', 'coffeescript', 'common+lisp', 'coq', 'crystal', 'css', 'cuda', 'dart', 'digital+command+language', 'dm', 'dockerfile', 'ejs', 'elixir', 'emacs+lisp', 'erlang', 'f%23', 'forth', 'fortran', 'freemarker', 'g-code', 'gdscript', 'gherkin', 'go', 'groovy', 'hack', 'handlebars', 'haskell', 'haxe', 'hcl', 'hlsl', 'html', 'java', 'javascript', 'jinja', 'julia', 'jupyter+notebook', 'kicad+layout', 'kotlin', 'lasso', 'less', 'logos', 'lua', 'm', 'makefile', 'markdown', 'matlab', 'mcfunction', 'mdx', 'nasal', 'nim', 'nix', 'nunjucks', 'objective-c', 'objective-c%2B%2B', 'ocaml', 'openedge+abl', 'openscad', 'pascal', 'perl', 'php', 'plpgsql', 'plsql', 'postscript', 'powershell', 'processing', 'pug', 'purebasic', 'python', 'qml', 'r', 'rescript', 'rich+text+format', 'robotframework', 'roff', 'ruby', 'rust', 'sass', 'scala', 'scss', 'shaderlab', 'shell', 'smarty', 'solidity', 'standard+ml', 'svelte', 'swift', 'tex', 'total_repos', 'tsql', 'twig', 'typescript', 'unrealscript', 'vba', 'verilog', 'vim+script', 'visual+basic+.net', 'vue', 'xslt', 'yacc', 'yaml', 'yara']
    lang = lang.strip().lower() if lang and isinstance(lang,str) and lang.strip().lower() in LANGUAGES else 'all'  # Convert language to lowercase if provided and valid
    language_dict = {}
    page_no = int(page_no) if page_no and isinstance(page_no,(str,int)) else 0
    for attempt in range(retries):  # Loop through the retry attempts
        try:
            
            url =  f'https://github.com/topics/{topic_id.lower().strip()}?{f"l={lang.lower().strip()}" if lang and lang.strip() else ""}{"&" if lang else ""}page={page_no}'
        
            response = requests.get(url,timeout=timeout)
            status_code = response.status_code
            if status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                topic_name = soup.find('h1').get_text().strip()
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
                languages = soup.find('details-menu',{'class':'select-menu-modal position-absolute'}).find_all('a', class_='select-menu-item')
                
                for language in languages:
                    lang_link = language.get('href') if language.get('href') else None
                    if lang_link :
                        for lang_id in  LANGUAGES:

                            if (lang_id != 'all' and f'https://github.com/topics/{topic_id.lower().strip()}?l={lang_id}&page={page_no}' == lang_link ) or (lang_id=='all' and f'https://github.com/topics/{topic_id.lower().strip()}?&page={page_no}'):
                                lang_text_tokens = language.find('span',{'class':'select-menu-item-text'}).get_text().strip().split() if language.find('span',{'class':'select-menu-item-text'}) else None
                                if lang_text_tokens:
                                    try:
                                        language_name = lang_text_tokens[0].lower().strip()
                                        
                                        language_counts = int(lang_text_tokens[-1].replace(',','').lower().strip())
                                        if language_name not in language_dict.keys() and language_counts:
                                            language_dict[lang_id] = {'name':language_name,'counts':language_counts}
                                        
                                    except:
                                        pass
                return {'error':False,'status_code':status_code,'topic': topic_id.lower().strip(), 'name':topic_name,'description': description, 'source': url, 'total_repos': language_dict[lang].get('counts',''), 'languages': [k for k,v in language_dict.items() if v.get('counts',0)],'lang':lang,'lang_name':language_dict[lang].get('name','')}
            else:
                return {'error':'StatusCode','status_code':status_code,'topic': topic_id.lower().strip(), 'name':topic_name,'description': description, 'source': url, 'total_repos':  language_dict[lang].get('counts',''), 'languages':  [k for k,v in language_dict.items() if v.get('counts',0)],'lang':lang,'lang_name':language_dict[lang].get('name','')}
            if attempt < retries - 1:
                time.sleep(delay)

        except Exception as e:  # Handle any exceptions that occur during the request or parsing
            error = e  # Print the error message for debugging (could be improved with proper logging)
            if attempt < retries - 1:
                time.sleep(delay)
    return {'error':error,'status_code':status_code, 'topic': topic_id,'name':topic_name, 'description': description, 'source': url, 'total_repos': total_repos, 'languages': {},'lang':lang, 'lang_name':''}  # Return an empty list if all retry attempts fail

