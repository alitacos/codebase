def get_google_learn_pathways_metadata_and_contents_of_url_article_via_requests_and_bs4(url:str='')->dict:
    """
    Extracts structured metadata and content from a Google Learn Pathways article page.

    This function fetches a Google Learn Pathways URL, parses the HTML content,
    and extracts key information such as breadcrumbs, title, introduction,
    and structured sections (including lessons and quizzes). It is designed
    specifically for pathway pages from domains like Google, Firebase, Android,
    Flutter, and Dart.

    Args:
        url (str): The URL of the Google Learn Pathways article to parse (must contain '/pathways/') (Defaults to '')

    Returns:
        dict: A dictionary containing extracted metadata including:
              - netloc: domain of the URL
              - path: URL path
              - lang: language parameter (if present)
              - breadcrumps: list of breadcrumb links and labels
              - title: main article title
              - intro: introductory text
              - index: list of sections with type, title, text, and action link

    Example usage:
        >>> result = get_google_learn_pathways_metadata_and_contents_of_url_article_via_requests_and_bs4(url='https://developers.google.com/learn/pathways')
    """

    import requests
    from bs4 import BeautifulSoup
    
    def get_url_parts(url:str='')->tuple:
        from urllib.parse import urlparse, parse_qs
        try:
            netloc = urlparse(url).netloc
            path = urlparse(url).path
            query = parse_qs(urlparse(url).query)
            language = query.get('hl', [""])[0]
            return netloc,path, query,language
        except Exception as e:
            return '','','',''
  
    def get_request(url:str='')->requests.Response|dict:
        try:
            return requests.get(url)            
        except Exception as e:
            return {'errors':[{e.__class__.__name__:str(e)}]} 
          
    def get_soup(response:requests.Response='')->'bs4.BeautifulSoup'|dict:
        try:
            return BeautifulSoup(response.content, 'html.parser')            
        except Exception as e:
            return {'errors':[{e.__class__.__name__:str(e)}]} 

    def get_main_article_element(soup:'bs4.BeautifulSoup'='')->'bs4.element.Tag'|None:
        try:
            return soup.find('article',{'class':'devsite-article'})            
        except Exception as e:
            return None
          
    def get_header_title(soup:'bs4.BeautifulSoup'='')->str:
        try:
            main_article_el =  soup.find('article',{'class':'devsite-article'})  or soup     
            header_element = main_article.find('div', {'class': 'devsite-playlist--header'})
            header = header_element.find(['h1','h2','h3']) if header_element and header_element.find(['h1','h2','h3']) else None
            return header.get_text() if header else ''         
        except Exception as e:
            return ''  
    def get_header_raw_text_content(soup:'bs4.BeautifulSoup'='')->str:
        try:
            main_article_el =  soup.find('article',{'class':'devsite-article'}) or soup  
            header_element = main_article.find('div', {'class': 'devsite-playlist--header'})
            if header_element:
                for tag in header_element.find_all(['h1','h2','h3','a']):
                    if tag.name in ['h1','h2','h3','a']:
                        tag.decompose()
            return header_element.get_text().strip() if  header_element and header_element.get_text()  else ''
        except Exception as e:
            return ''  

          
    def get_breadcrumps_list(soup:'bs4.BeautifulSoup'='')->list:
        try:
            main_article = soup.find('article',{'class':'devsite-article'}) or soup            
            breadcrumb_element = main_article.find('ul',{'aria-label':'Breadcrumb'}) or main_article.find('ul',{'class':'devsite-breadcrumb-list'})
            return [{'href':i.get('href').strip(),'text':i.get_text().strip()} for i in breadcrumb.find_all('a') if i and i.get_text() and i.get('href')]
          
        except Exception as e:
            return []

  
    def get_dev_playlist_type_title_and_contents_strings(dev_playlist:'bs4.element.Tag'=None)->tuple:
        try:
            IsType = dev_playlist.get('type',None)
            title,content = None, None
            if IsType == 'quiz':
                title = dev_playlist.find('h2').get_text() if dev_playlist and dev_playlist.find('h2') else None
                dev_playlist.find('h2').decompose() if dev_playlist and dev_playlist.find('h2') else None
                content = dev_playlist
            else:
                title = dev_playlist.find('div',{'class':'devsite-playlist--item-top-title'}).get_text() if dev_playlist and dev_playlist.find('div',{'class':'devsite-playlist--item-top-title'}) else None
                content = dev_playlist.find('div',{'class':'devsite-playlist--item--content'})
                #index_no = dev_playlist.find('div',{'class':'devsite-playlist--item-top-index'})
            return IsType.strip() if IsType else '', title.get_text().strip() if title else '', content.get_text().strip() if content else '' 
        except Exception as e:
            return '','',''    
          
    def get_action_link(dev_playlist:'bs4.element.Tag'='',netloc:str='')->list:
        try:
            actions_element = dev_playlist.find('div',{'class':'devsite-playlist--item--actions'}).find('a') if dev_playlist and dev_playlist.find('div',{'class':'devsite-playlist--item--actions'}) else None
            action_link = actions.get('href','') if actions_element and actions_element.get('href') else ''
            action_link = action_link.strip().strip('/') if action_link else ''
            if action_link:
                
                if not action_link.startswith('http') and netloc:
                    action_link = f"{netloc.strip().strip('/')}/{action_link}"
            return action_link.strip() if action_link else ''
        except Exception as e:
            return ""
          
    def get_dev_playlists(soup:"bs4.BeautifulSoup"=None)->list:
        try:
            main_article = soup.find('article',{'class':'devsite-article'}) or soup
            dev_playlist_main = main_article.find('devsite-playlist').find('div',{'class':'devsite-playlist--sections'}) if main_article else None
            return dev_playlist_main.find_all('div',{'class':'devsite-playlist--section'}) if dev_playlist_main else None

        except Exception as e:
            return None
    def get_sections(dev_playlists:list=None)->list:
        sections = []
        try:
            if dev_playlists:
                for dev_playlist in dev_playlists:
                    try:
                        dev_playlist_type , dev_playlist_title, dev_playlist_raw = get_dev_playlist_type_title_and_contents_strings(dev_playlist)
                        action_link = get_action_link(dev_playlist =dev_playlist,netloc=url_netloc)
                        dev_playlist_type = dev_playlist_type.strip() if dev_playlist_type else ""
                        dev_playlist_title = dev_playlist_title.strip() if dev_playlist_title else ""
                        dev_playlist_raw = '\n'.join([i.strip() for i in dev_playlist_raw.get_text().strip().split('\n') if i and i.strip()]) if dev_playlist_raw and dev_playlist_raw.get_text()  else ""
                        action_link = action_link.strip() if action_link else ""
                        if dev_playlist_raw or (dev_playlist_title and action_link):                      
                            item = {'type':dev_playlist_type, 'title':dev_playlist_title , 'text':dev_playlist_raw,'link': action_link }
                            if item not in sections:
                                sections.append(item)
                    except Exception as e1:
                        continue
              return sections
        except Exception as e:
            return None

 
          
    response = get_request(url)
    soup = get_soup(url) if not isinstance(response,dict) else None
    main_article_el = get_main_article_element(soup) if soup and not isinstance(soup, dict) else None
    breadcrumbs = get_breadcrumps_list(soup) if soup and not isinstance(soup, dict) else None
    header_title = get_header_title(soup) if soup and not isinstance(soup, dict) else None#if added soup directly should also work, this is why i wrote in functions soup.find('article',{'class':'devsite-article'}) or soup
    header_raw_text_content = get_header_raw_text_content(soup) if soup and not isinstance(soup, dict) else None
    url_netloc, url_path,url_query, url_lang = get_url_parts(url)
    dev_playlists = get_dev_playlists(soup) if soup and not isinstance(soup, dict) else None
    sections = get_sections(dev_playlists) if soup and not isinstance(soup, dict) and dev_playlists else None
    error_reasons = []
    if not url:
        error_reasons.append({'ValueError':'empty URL string'})
    if url and not '/pathways/' in url or not  any(x in url for x in ['google', 'firebase', 'android', 'flutter', 'dart']):  
        error_reasons.append({'ValueError':"url contains not 'google', 'firebase', 'android', 'flutter' or 'dart' "})
    if not response:
        error_reasons.append({"NotFoundError":"requests get method could not be resoled"})
    if not soup:
        error_reasons.append({"NotFoundError":"BeautifulSoup element could not be resoled"})
    if isinstance(response, dict):
        error_reasons.extend(response.get('errors',[]))
    if isinstance(soup, dict):
        error_reasons.extend(soup.get('errors',[]))
    if not main_article_el:
        error_reasons.append({"NotFoundError":"main article container was not found in HTML"})
    if not header_title:
        error_reasons.append({"NotFoundError":'title not found'})
    if not breadcrumbs:
        error_reasons.append({"NotFoundError":'breadcrumbs not found'})
    if not header_raw_text_content:
        error_reasons.append({"NotFoundError":'intro section not found'})
    if not sections:
        error_reasons.append({"NotFoundError":'no sections found'})
    if not url_lang:
        error_reasons.append({"NotFoundError":'no language found in url'})
      
    return {'errors':error_reasons, 'netloc':current_netloc,'path':url_query,'lang':url_lang ,'breadcrumps':breadcrumps, 'title':header_title, 'intro':header_raw_text_content ,'index':sections}