def build_github_topics_query_url(topic:str='',lang:str='', page_no:int=0)->str:
    """
    Build a GitHub Topics query URL using a topic, programming language, and page number.

    Args:
        topic (str): GitHub topic name used in the Topics URL.
        lang (str): Programming language name or GitHub language value used as
            the language filter.
        page_no (int): GitHub Topics page number to include in the URL.

    Returns:
        str: GitHub Topics query URL, or an empty string when no topic is provided.

    Example Usage:
        >>> build_github_topics_query_url(topic="windows", lang="Python", page_no=2) #[out]: 'https://github.com/topics/windows?l=python&page=2'
    """
    if not topic or not topic.strip():
        return ''
    try:
        page_no = int(page_no)
    except Exception:
        page_no = 0
    try:
        langstring = ''
        for k,v in  {'Python':'python' , 'Vue':'vue', 'BASIC':'basic', 'Haskel':'haskel', 'CSS':'css', 'Lua':'lua', 'EJS':'ejs', 'XSLT':'xslt', 'SCSS':'scss', 'ruby':'ruby', 'Jupyter Notebook':'jupyter+notebook', 'HTML':'html', 'Makefile':'makefile', 'PowerShell':'powershell', 'Objective-C':'objective-c', 'JavScript':'javascript', 'Flutter':'flutter', 'Kotlin':'kotlin', 'Dart':'dart', 'Batchfile':'batchfile', 'Rust':'rust', 'Scala':'scala', 'PHP':'php', 'TypeScript':'typescript', 'Swift':'swift', 'Tex':'tex', 'Julia':'julia', 'MATLAB':'matlab', 'OpenQASM':'openqasm', 'R':'r', 'Wolfram Language':'wolfram+language', 'Dockerfile':'dockerfile', 'Go':'go', 'Visual Basic.NET':'visual+basic+.net', 'Assembly':'assembly', 'Pascal':'pascal', 'CSS':'css', 'C':'c', 'Java':'java', 'C#':'c%23', 'Gleam':'gleam', 'Elixir':'elixir', 'Erlang':'erlang', 'Svelte':'svelte', 'MDX':'mdx', 'F#':'f%23', 'F#':'f%23', 'Shell':'shell', 'Astro':'astro', 'TSQL':'tsql', 'PLpgSQL':'plpgsql' 'C++':'c%2B%2B'}.items():
            if lang.lower().strip() == k.lower() or lang.lower().strip() == v.lower():
                langstring = v
                break
    except Exception:
        langstring = ''
    
        
    url = f"https://github.com/topics/{topic.strip()}"
    if not langstring and not page_no:
        return url
    if page_no and not langstring:
        return f'{url}?page={int(page_no)}'
    if not page_no and langstring:
        return f'{url}?l={int(langstring)}'
    if page_no and langstring:
        return f'{url}?l={int(langstring)}&page={page_no}'
    return ''
