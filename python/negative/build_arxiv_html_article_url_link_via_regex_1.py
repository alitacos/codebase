def build_arxiv_html_article_url_link_via_regex(url: str = '', mode: str = 'html') -> str:#negative
    import re
    try:
        url = url.strip()
        if not url:
            return ''

        # Normalize protocol/domain
        
        url = 'https://' + url if not url.startswith(('https://','http://')) else url
        # Extract ID from URL or accept ID directly
        match = re.fullmatch( r'(?:https?://arxiv\.org/(?:html|pdf|abs)/)?(\d+\.\d+(?:v\d+)?)\/?', url )
        return f'https://arxiv.org/{mode}/{match.group(1)}' if match else ''

    except Exception:
        return ''
