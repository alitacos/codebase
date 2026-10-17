def check_german_district_by_key_via_OpenPLZ_api_via_requests_and_no_retries(query:str='')->dict:
    """     Fetch districts from OpenPLZ API by federal state input (name, abbreviation, or key). Accepts input as string or int.    """
    import requests
    federal_states = [{"ags": "01", "name": "Schleswig-Holstein", "short": "SH",'iso-3166-2':'DE-SH'},{"ags": "02", "name": "Hamburg", "short": "HH",'iso-3166-2':'DE-HH'},{"ags": "03", "name": "Niedersachsen", "short": "NI",'iso-3166-2':'DE-NI'},{"ags": "04", "name": "Bremen", "short": "HB",'iso-3166-2':'DE-HB'},{"ags": "05", "name": "Nordrhein-Westfalen", "short": "NW",'iso-3166-2':'DE-NW'},{"ags": "06", "name": "Hessen", "short": "HE",'iso-3166-2':'DE-HE'},{"ags": "07", "name": "Rheinland-Pfalz", "short": "RP",'iso-3166-2':'DE-RP'},{"ags": "08", "name": "Baden-Württemberg", "short": "BW",'iso-3166-2':'DE-BW'},{"ags": "09", "name": "Bayern", "short": "BY",'iso-3166-2':'DE-BY'},{"ags": "10", "name": "Saarland", "short": "SL",'iso-3166-2':'DE-SL'},{"ags": "11", "name": "Berlin", "short": "BE",'iso-3166-2':'DE-BE'},{"ags": "12", "name": "Brandenburg", "short": "BB",'iso-3166-2':'DE-BB'},{"ags": "13", "name": "Mecklenburg-Vorpommern", "short": "MV",'iso-3166-2':'DE-MV'},{"ags": "14", "name": "Sachsen", "short": "SN",'iso-3166-2':'DE-SN'},{"ags": "15", "name": "Sachsen-Anhalt", "short": "ST",'iso-3166-2':'DE-ST'},{"ags": "16", "name": "Thüringen", "short": "TH",'iso-3166-2':'DE-TH'}]
    timezone_cet = 'Central European Time'
    timezone = {'zone':'Europe/Berlin', 'CET':'UTC+1','CEST':'UTC+2'}
    # Convert int input to string with leading zero if needed
    try:
        if isinstance(query, int):
            query = f"{query:02d}"
        if not isinstance(query, int):
            query = str(query).strip().lower().replace("ü", "u").replace("ä", "a").replace("ö", "o")
        state_key = None
        for state in federal_states:
            if query == state["ags"] or query == state["ags"].lstrip("0") or query == state["name"].lower().replace("ü", "u").replace("ä", "a").replace("ö", "o") or query == state["short"].lower():
                state_key = state["ags"]
                break
        if not state_key:
            return {'error':f'Could not resolve input', 'status':None,'query':query, 'data':response.json()}
            response = requests.get(f'https://openplzapi.org/de/FederalStates/{state_key}/Districts')
            if response.status_code == 200:
                return {'error':False, 'status':response.status_code,'query':query, 'data':response.json()}
            return {'error':f'unexpected status code {response.status_code}',  'status':response.status_code,'query':query,'data':[]}
    except Exception as e:
        return {'error':f'{str(e)},{e.__class__.__name__}', 'status':None, 'query':query,'data':[]}
# Example usage:
#print(check_german_district_by_key_via_OpenPLZ_api_via_requests_and_no_retries(8))          # int input, will be '08'
#print(check_german_district_by_key_via_OpenPLZ_api_via_requests_and_no_retries('08'))       # string with leading zero
#print(check_german_district_by_key_via_OpenPLZ_api_via_requests_and_no_retries('8'))        # string without leading zero
#print(check_german_district_by_key_via_OpenPLZ_api_via_requests_and_no_retries('BW'))       # abbreviation
#print(check_german_district_by_key_via_OpenPLZ_api_via_requests_and_no_retries('baden-wurttemberg'))  # full name (with simplified umlaut)
#out: [{'key': '08111', 'name': 'Stuttgart, Stadtkreis', 'type': 'Stadtkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Stuttgart'}, {'key': '08115', 'name': 'Böblingen', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Böblingen'}, {'key': '08116', 'name': 'Esslingen', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Esslingen am Neckar'}, {'key': '08117', 'name': 'Göppingen', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Göppingen'}, {'key': '08118', 'name': 'Ludwigsburg', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Ludwigsburg'}, {'key': '08119', 'name': 'Rems-Murr-Kreis', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Waiblingen'}, {'key': '08121', 'name': 'Heilbronn, Stadtkreis', 'type': 'Stadtkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Heilbronn'}, {'key': '08125', 'name': 'Heilbronn', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Heilbronn'}, {'key': '08126', 'name': 'Hohenlohekreis', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Künzelsau'}, {'key': '08127', 'name': 'Schwäbisch Hall', 'type': 'Landkreis', 'governmentRegion': {'key': '081', 'name': 'Reg.-Bez. Stuttgart'}, 'federalState': {'key': '08', 'name': 'Baden-Württemberg'}, 'administrativeHeadquarters': 'Schwäbisch Hall'}]
