def extract_profiles_over_postal_code_via_kaufmich_com_api(postal_code:str='')->dict:
    import requests
    BASE_URL = "https://api.kaufmich.com/api/v2"
    HEADERS = {"Accept": "application/json","Content-Type": "application/json;charset=UTF-8","User-Agent": "Mozilla/5.0"}
    if not postal_code:
        return {}
    def autocomplete_location(user_input:str='')->list:
        try:
            url = f"{BASE_URL}/search/city/autocomplete"
            payload = {"input": user_input,"active_only": True}
            response = requests.post(url, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json().get("data", [])
            return data
        except Exception as e:
            return {}
    def find_exact_location(data:list=[], user_input:str='')->dict:
        # Normalize input to lowercase for comparison
        user_input_norm = user_input.strip().lower()
        for entry in data:
            # Match on postal code or normalized city name
            if user_input_norm == entry.get("zip_trim", "").lower() or user_input_norm == entry.get("city_modified", "").lower():
                return entry
        return None
    def search_profiles_for_page(lat:str='', lon:str='', radius:int=5, page_no:int=1, page_size:int=24)->dict:
        #max :page_size = 24,min page_size=1
        if not lat and not lon:
            return {}
        try:
            url = f"{BASE_URL}/search"
            payload = {"page_no": page_no,"page_size": page_size,"query": {},"filterquery": {"user_type": [2],"location": {"lat": lat,"lon": lon,"radius": radius}},"facets": {"term": ["figure_type","cup_size","hair_color","hair_length","intimate_hair","sexuality","race_type","customer_type","meeting_option","body_hair","escort_service","partner_preference","escort_service_soft","escort_service_hard","escort_service_clothing","escort_service_fetish","breast_type","escort_primary_service","client_primary_service","gender_identity","escort_service_tags","piercing_tattoo","breast_type","piercing","tattoo","is_smoker","gender","languages","nationality","country","is_available_now","is_visible","has_avatar","is_verified","is_new","is_phone_show","has_price","has_review","is_hot","has_fsk18_photos","is_member","on_tour","exclusive_content","price_15_mins","price_30_mins","price_60_mins","price_120_mins","price_180_mins","price_240_mins","price_480_mins","price_720_mins","price_1440_mins"],"range": {"age": ["[18,25]", "[26,35]", "[36,45]", "[46,*]"]}},"sort": "top_ranking"}
            response = requests.post(url, headers=HEADERS, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            return {}
    def search_kaufmich_com_profiles(lat, lon)->list:
        record  = search_profiles(lat, lon,radius=5, page_no=1, page_size=24)
        data = record.get('data',[]) if record and isinstance(record,dict) else []
        try:
            totalpages = int(record.get('meta',{}).get('total',''))/24
            totalpages = int(totalpages)+1 if int(totalpages) < totalpages else totalpages
        except Exception as e:
            totalpages = 0
        if totalpages > 1:
            for pagenum in list(range(2,totalpages+1)):
                record  = search_profiles(lat, lon,radius=5, page_no=pagenum, page_size=24)
                subdata = record.get('data',[]) if record and isinstance(record,dict) else []
                data.extend(subdata)
        return data
    locations = autocomplete_location(postal_code)
    locations = find_exact_location(locations, postalcode)
    lat,lon = locations.get('lat',''),locations.get('lon','')
    return search_kaufmich_com_profiles(lat, lon)
