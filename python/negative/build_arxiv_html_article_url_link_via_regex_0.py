def build_arxiv_html_article_url_link_via_regex(url: str = '', mode: str = 'html') -> str:
    import re
    try:
        url = url.strip()
        if not url:
            return ''

        # Normalize protocol/domain
        
        url = 'https://' + url if not url.startswith(('https://','http://')) else url
        # Extract ID from URL or accept ID directly
        match = re.fullmatch( r'(?:https?://arxiv\.org/(?:html|pdf|abs)/)?' r'(\d+\.\d+(?:v\d+)?)' r'(?:/)?' r'(?:#[^/]*)?', url ) if url and len(url.strip().split()) == 1 else None
        match = re.fullmatch( r'(?:https?://arxiv\.org/(?:html|pdf|abs)/)?' r'(\d+\.\d+(?:v\d+)?)' r'/?(?:#.*)?', url )  if url and len(url.strip().split()) == 1 else None
        return f'https://arxiv.org/{mode}/{match.group(1)}' if match else ''

    except Exception:
        return ''