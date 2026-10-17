def build_arxiv_html_article_url_link_via_regex(
    url: str = '', mode: str = 'html'
) -> str:
    import re

    try:
        url = url.strip()
        if not url or len(url.split()) != 1:
            return ''

        url = 'https://' + url if not url.startswith(('https://', 'http://')) else url

        match = re.fullmatch(
            r'(?:https?://arxiv\.org/(?:html|pdf|abs)/)?'
            r'(\d+(?:v\d*)?\.\d+(?:v\d*)?)'
            r'/?'
            r'(?:#.*)?',
            url
        )

        if not match:
            return ''

        uiid = match.group(1)

        # Equivalent to:
        # not uiid.replace('.').replace('v').isdigit()
        # uiid.count('v') > 1
        # uiid.count('.') != 1
        if uiid.count('v') > 1:
            return ''

        return f'https://arxiv.org/{mode}/{uiid}'

    except Exception:
        return ''