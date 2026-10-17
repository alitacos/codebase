def get_metadata_of_topic_in_github_via_requests_and_bs4(topic_id:str='',lang:str=None,page_no:int=0, retries:int=1,delay:int=2,timeout:int=3, **kwargs):
    import requests
    from bs4 import BeautifulSoup
    import time
    from urllib.parse import quote, unquote
    import re
    LANGUAGES=['abap', 'actionscript', 'adblock+filter+list', 'all', 'angelscript', 'antlr', 'apex', 'api+blueprint', 'applescript', 'asl', 'asp.net', 'assembly', 'astro', 'autohotkey', 'autoit', 'awk', 'basic', 'batchfile', 'bitbake', 'blade', 'c', 'c#', 'c++', 'cirru', 'classic+asp', 'clojure', 'cmake', 'coffeescript', 'common+lisp', 'coq', 'crystal', 'css', 'cuda', 'dart', 'digital+command+language', 'dm', 'dockerfile', 'ejs', 'elixir', 'emacs+lisp', 'erlang', 'f#', 'forth', 'fortran', 'freemarker', 'g-code', 'gdscript', 'gherkin', 'go', 'groovy', 'hack', 'handlebars', 'haskell', 'haxe', 'hcl', 'hlsl', 'html', 'java', 'javascript', 'jinja', 'julia', 'jupyter+notebook', 'kicad+layout', 'kotlin', 'lasso', 'less', 'logos', 'lua', 'm', 'makefile', 'markdown', 'matlab', 'mcfunction', 'mdx', 'nasal', 'nim', 'nix', 'nunjucks', 'objective-c', 'objective-c++', 'ocaml', 'openedge+abl', 'openscad', 'pascal', 'perl', 'php', 'plpgsql', 'plsql', 'postscript', 'powershell', 'processing', 'pug', 'purebasic', 'python', 'qml', 'r', 'rescript', 'rich+text+format', 'robotframework', 'roff', 'ruby', 'rust', 'sass', 'scala', 'scss', 'shaderlab', 'shell', 'smarty', 'solidity', 'standard+ml', 'svelte', 'swift', 'tex', 'total_repos', 'tsql', 'twig', 'typescript', 'unrealscript', 'vba', 'verilog', 'vim+script', 'visual+basic+.net', 'vue', 'xslt', 'yacc', 'yaml', 'yara']

    # Helper function to extract and unquote the language from a GitHub topic filter link
    def get_lang_from_github_link(link: str) -> str | None:
        match = re.search(r'l=([^&]+)', link)
        if match:
            return unquote(match.group(1))
        # If 'l=' is not in the link, and it's a page link, it might be the 'all' option
        elif 'page=' in link and 'l=' not in link:
            return 'all'
        return None

    if not topic_id or not isinstance(topic_id, str) or not topic_id.strip():
        return []
    


    # Determine the 'effective_lang_key' (the key to be used for language_dict and URL construction)
    effective_lang_key = 'all' # Default
    if lang and isinstance(lang, str) and lang.strip():
        # Normalize input lang to match potential keys (e.g., 'c++' or 'jupyter+notebook')
        normalized_input_lang = lang.strip().lower().replace(' ', '+')

        # Check if the normalized input lang exists in our LANGUAGES list (case-insensitive for lookup)
        # The key stored in language_dict should be the normalized_input_lang (e.g. 'python', 'c++')
        if any(normalized_input_lang == l.lower().replace(' ', '+') for l in LANGUAGES):
            effective_lang_key = normalized_input_lang
        elif normalized_input_lang == 'all':
            effective_lang_key = 'all'

    description, total_repos_header, url, status_code, topic_name = None, None, None, None, None
    language_dict = {} # Stores extracted language data from the page's filter menu (key: unquoted lang name)
    page_no = int(page_no) if page_no and isinstance(page_no, (str, int)) else 0

    for attempt in range(retries):
        try:
            # Construct the URL for the request
            encoded_topic_id = quote(topic_id.lower().strip())
            # Ensure the lang parameter in the URL is properly quoted
            lang_param_for_url = f"l={quote(effective_lang_key)}" if effective_lang_key != 'all' else ""
            separator = "&" if lang_param_for_url else ""
            request_url = f'https://github.com/topics/{encoded_topic_id}?{lang_param_for_url}{separator}page={page_no}'

            response = requests.get(request_url, timeout=timeout)
            status_code = response.status_code
            url = request_url # Store the URL actually requested

            if status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                topic_name_element = soup.find('h1')
                topic_name = topic_name_element.get_text().strip() if topic_name_element else ""

                description_element = soup.find('div', class_='markdown-body')
                if description_element is not None:
                    desc_p = description_element.find('p')
                    description = desc_p.text.strip() if desc_p else ""
                else:
                    description = ''

                # Extract total repository count from the main header
                total_repos_element = soup.find('h2', class_='h3 color-fg-muted')
                if total_repos_element is not None:
                    total_repos_text = total_repos_element.text.strip()
                    count_match = re.search(r'([\d,]+)', total_repos_text)
                    if count_match:
                        total_repos_header = int(count_match.group(1).replace(',', ''))
                    else:
                        total_repos_header = 0
                else:
                    total_repos_header = 0

                # Populate language_dict from the 'languages' filter dropdown
                languages_menu = soup.find('details-menu', {'class': 'select-menu-modal position-absolute'})
                if languages_menu:
                    languages_items = languages_menu.find_all('a', class_='select-menu-item')
                    for language_item in languages_items:
                        lang_link = language_item.get('href')
                        if lang_link:
                            # Extract the language key (unquoted) from the filter link
                            current_linked_lang_key = get_lang_from_github_link(lang_link)

                            if current_linked_lang_key: # Only process if a valid language key was extracted
                                lang_text_tokens_element = language_item.find('span', {'class': 'select-menu-item-text'})
                                if lang_text_tokens_element:
                                    full_text = lang_text_tokens_element.get_text().strip()

                                    # Extract count using regex (e.g., "Python 2,622")
                                    count_match_in_text = re.search(r'([\d,]+)$', full_text) # Look for numbers at the end
                                    language_counts_extracted = 0
                                    language_name_displayed = ""

                                    if count_match_in_text:
                                        try:
                                            language_counts_extracted = int(count_match_in_text.group(1).replace(',', ''))
                                            # Remove count and comma from the full text to get the name
                                            language_name_displayed = full_text.replace(count_match_in_text.group(0), '').strip()
                                        except ValueError:
                                            pass
                                    else: # If no count found (e.g., "All"), assume the whole text is the name
                                        language_name_displayed = full_text.strip()

                                    if language_name_displayed and current_linked_lang_key not in language_dict: # Add if not already present
                                        language_dict[current_linked_lang_key] = {'name': language_name_displayed, 'counts': language_counts_extracted}

                # Assemble the return result based on the 'effective_lang_key'
                result_total_repos = 0
                result_lang_name = ""
                # List of actual languages found in menu, excluding 'all', in their unquoted format
                result_languages_list = [k for k in language_dict.keys() if k != 'all']

                if effective_lang_key == 'all':
                    result_total_repos = total_repos_header # From the main header
                    result_lang_name = 'all'
                elif effective_lang_key in language_dict:
                    result_total_repos = language_dict[effective_lang_key]['counts']
                    result_lang_name = language_dict[effective_lang_key]['name']
                else:
                    # Specific language requested but not found in the page's filter menu or LANGUAGES list
                    result_total_repos = 0
                    # Use the requested key, it might not be a valid display name if not found
                    result_lang_name = effective_lang_key

                return {'error': False, 'status_code': status_code, 'topic': topic_id.lower().strip(),
                        'name': topic_name, 'description': description, 'source': url,
                        'total_repos': result_total_repos, 'languages': result_languages_list,
                        'lang': effective_lang_key, 'lang_name': result_lang_name}
            else:
                # Handle non-200 status codes
                return {'error': 'StatusCode', 'status_code': status_code, 'topic': topic_id.lower().strip(),
                        'name': topic_name, 'description': description, 'source': request_url,
                        'total_repos': total_repos_header, 'languages': [], # No language counts if page error
                        'lang': effective_lang_key, 'lang_name': ""}

            if attempt < retries - 1:
                time.sleep(delay)

        except Exception as e:
            error = e
            if attempt < retries - 1:
                time.sleep(delay)
    # Return error if all retries fail
    return {'error': error, 'status_code': status_code, 'topic': topic_id, 'name': topic_name,
            'description': description, 'source': url, 'total_repos': total_repos_header, 'languages': [],
            'lang': effective_lang_key, 'lang_name': ''}

