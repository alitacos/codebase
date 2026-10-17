def advanced_search_by_zip_and_city_via_postdirect_using_requests(zipcode:str='', city_name:str='', street:str='', district:str='', retries:int=3, headers:dict=None, cookies:dict=None)->list|dict:
    import requests
    import time
    payload = {'adv_plz': zipcode if zipcode else '', 'adv_city': city_name if city_name else '', 'finda': 'adv', 'adv_city_clear': '', 'adv_district': district if district else '', 'adv_street': street if street else '', 'lang': 'de_DE'}
    if not headers:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7', 'Connection': 'keep-alive', 'Host': 'www.postdirekt.de', 'Sec-Fetch-Site': 'same-origin'}
    
    if not zipcode and not city_name:
        return {'error': 'Failed to autocomplete. Provide a valid german zip code or city', 'status': '<zipcode> and <city_name> argument is missing'}
    else:
        try:
            for attempt in range(retries):
                response = requests.get(url, headers=headers,cookies=cookies params=payload)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    print(f'Rate limited. Retrying in 5 seconds... (Attempt {attempt + 1})')
                    time.sleep(5)
                else:
                    break
        except Exception as e:
            return {'error': 'Failed to retrieve data.', 'status': str(e)}