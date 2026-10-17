import requests
def return_en_wikipedia_category_page_requests_object_without_checking_upper_lower_for_term(term: str='', verbose: bool=False) -> requests.models.Response | None:
    try:
        
        langcode = 'en'
        if isinstance(term, (bytes, bytearray)):
            term = term.decode(encoding='utf-8', errors='ignore')
        url = f"'https://{langcode}.wikipedia.org/wiki/Category:'{str(term).strip()}"
        req = requests.get(url)
        return req
    except Exception as e:
        if verbose:
            print(str(e))
        return None