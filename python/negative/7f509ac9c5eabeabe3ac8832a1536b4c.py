def query_rapit_api_google_search_74_via_http_client(token: str='', query: str='', limit: str='', rel_keys: bool=True):
    import http.client
    conn = http.client.HTTPSConnection('google-search74.p.rapidapi.com')
    headers = {'x-rapidapi-key': 'a4e6dccb98mshfa6fce6b9ec8cefp1148bdjsnf09487a39199', 'x-rapidapi-host': 'google-search74.p.rapidapi.com'}
    conn.request('GET', '/?query=Nike%20ser&limit=10&related_keywords=true', headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode('utf-8')
